import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_governance import BODY


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_gate():
    spec = importlib.util.spec_from_file_location("governance_gate", SCRIPTS / "governance_gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


POLICY = {"repository": "owner/project", "authorized_reviewers": ["reviewer"],
          "max_added_lines": 10, "max_net_growth_lines": 5,
          "max_binary_files": 0, "excluded_paths": []}
HEAD = "b" * 40
BASE = "a" * 40
PR = {"number": 7, "state": "open", "body": BODY, "user": {"login": "author"},
      "head": {"sha": HEAD}, "base": {"sha": BASE, "repo": {"full_name": "owner/project"}}}


def approval(login="reviewer", state="APPROVED", sha=HEAD, identifier=1, kind="User"):
    return {"id": identifier, "user": {"login": login, "type": kind}, "state": state,
            "commit_id": sha, "submitted_at": "2026-10-28T00:00:00Z"}


class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = load_gate()

    def check(self, reviews=None, permissions=None, pr=None, policy=None, raw=b"2\t1\tfile.py\0"):
        return self.gate.evaluate(pr or PR, [approval()] if reviews is None else reviews,
                                  {"reviewer": "write"} if permissions is None else permissions,
                                  raw, policy or POLICY)

    def test_real_review_record_and_small_diff_pass(self):
        result = self.check()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["approved_by"], ["reviewer"])
        self.assertEqual(result["counted"]["net_growth"], 1)

    def test_missing_approval_fails_despite_body_marker(self):
        pr = copy.deepcopy(PR)
        pr["body"] += "\nReviewer approved: reviewer; APPROVED=true\n"
        self.assertTrue(self.check(reviews=[], pr=pr)["errors"])

    def test_closed_or_missing_pr_state_cannot_pass_as_current_approval(self):
        for state in ("closed", None):
            with self.subTest(state=state):
                self.assertTrue(self.check(pr=dict(PR, state=state))["errors"])

    def test_invalid_reviewer_identities_and_access_fail(self):
        for login, kind, permission in (("author", "User", "write"), ("owner", "User", "admin"),
                                        ("stranger", "User", "write"), ("reviewer", "Bot", "write"),
                                        ("reviewer", "User", "read"), ("reviewer", "User", "none")):
            with self.subTest(login=login, kind=kind, permission=permission):
                self.assertTrue(self.check(reviews=[approval(login=login, kind=kind)],
                                           permissions={login: permission})["errors"])

    def test_stale_approval_is_invalid_after_new_commit(self):
        self.assertTrue(self.check(reviews=[approval(sha=BASE)])["errors"])

    def test_last_decisive_review_wins_and_comments_do_not_revoke(self):
        for state in ("CHANGES_REQUESTED", "DISMISSED"):
            with self.subTest(state=state):
                self.assertTrue(self.check(reviews=[approval(), approval(state=state, identifier=2)])["errors"])
        self.assertFalse(self.check(reviews=[approval(), approval(state="COMMENTED", identifier=2)])["errors"])
        self.assertFalse(self.check(reviews=[approval(state="CHANGES_REQUESTED"), approval(identifier=2)])["errors"])

    def test_missing_evidence_fails_even_with_valid_approval(self):
        pr = copy.deepcopy(PR)
        pr["body"] = "## Summary\nApproved and tests passed.\n"
        self.assertTrue(self.check(pr=pr)["errors"])

    def test_growth_limits_are_enforced_independently(self):
        self.assertTrue(self.check(raw=b"11\t10\tfile.py\0")["errors"])
        self.assertTrue(self.check(raw=b"6\t0\tfile.py\0")["errors"])
        self.assertFalse(self.check(raw=b"10\t5\tfile.py\0")["errors"])

    def test_exclusions_are_explicit_and_renames_need_both_paths(self):
        policy = dict(POLICY, excluded_paths=["generated/*"])
        result = self.check(policy=policy, raw=b"20\t0\tgenerated/data.txt\0")
        self.assertFalse(result["errors"])
        self.assertEqual(result["total"]["added"], 20)
        self.assertEqual(result["counted"]["added"], 0)
        self.assertTrue(self.check(policy=policy, raw=b"20\t0\t\0src/code.py\0generated/code.py\0")["errors"])

    def test_binary_changes_and_malformed_numstat_fail_closed(self):
        self.assertTrue(self.check(raw=b"-\t-\timage.png\0")["errors"])
        for raw in (b"2\t1\tfile.py", b"x\t1\tfile.py\0", b"1\t2\t\0old\0"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.check(raw=raw)

    def test_policy_rejects_invalid_values_and_unknown_keys(self):
        for key, value in (("max_added_lines", -1), ("max_added_lines", True),
                           ("max_net_growth_lines", "5"), ("authorized_reviewers", []),
                           ("excluded_paths", ["*"]), ("unknown", 1)):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.gate.validate_policy(dict(POLICY, **{key: value}))

    def test_malformed_review_does_not_satisfy_approval(self):
        for value in ({}, {"user": None}, dict(approval(), id="1"), dict(approval(), commit_id=None)):
            with self.subTest(value=value):
                self.assertTrue(self.check(reviews=[value])["errors"])

    def test_github_cli_adapter_flattens_pages_and_sanitizes_errors(self):
        completed = subprocess.CompletedProcess([], 0, json.dumps([[approval()], []]), "")
        with patch.object(self.gate.subprocess, "run", return_value=completed):
            self.assertEqual(self.gate.GitHub("owner/project").reviews(7), [approval()])
        completed = subprocess.CompletedProcess([], 1, "PRIVATE_RESPONSE", "SECRET_TOKEN")
        with patch.object(self.gate.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(ValueError, "GitHub API") as error:
                self.gate.GitHub("owner/project").reviews(7)
            self.assertNotIn("SECRET_TOKEN", str(error.exception))
            self.assertNotIn("PRIVATE_RESPONSE", str(error.exception))


class GitDiffTests(unittest.TestCase):
    def test_actual_git_diff_counts_lines_and_handles_renames(self):
        gate = load_gate()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()

            git("init", "-q")
            git("config", "user.name", "Test fixture")
            git("config", "user.email", "fixture@example.invalid")
            (root / "old.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "Base")
            base = git("rev-parse", "HEAD")
            git("mv", "old.txt", "new name.txt")
            (root / "added.txt").write_text("four\nfive\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "Rename and add")
            head = git("rev-parse", "HEAD")
            result = gate.evaluate(dict(PR, head={"sha": head}, base={"sha": base, "repo": {"full_name": "owner/project"}}),
                                   [approval(sha=head)], {"reviewer": "write"}, gate.git_diff(root, base, head), POLICY)
            self.assertFalse(result["errors"])
            self.assertEqual(result["total"], {"added": 2, "deleted": 0, "net_growth": 2, "binary_files": 0})

    def test_orchestration_uses_live_body_reviews_and_rechecks_revision(self):
        gate = load_gate()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()

            git("init", "-q")
            git("config", "user.name", "Test fixture")
            git("config", "user.email", "fixture@example.invalid")
            (root / "file.txt").write_text("base\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "Base")
            base = git("rev-parse", "HEAD")
            (root / "file.txt").write_text("base\nnew\n", encoding="utf-8")
            git("commit", "-qam", "Head")
            head = git("rev-parse", "HEAD")
            pr = copy.deepcopy(PR)
            pr["head"]["sha"], pr["base"]["sha"] = head, base
            event = {"pull_request": copy.deepcopy(pr), "repository": {"full_name": "owner/project"}}
            event["pull_request"]["body"] = "Stale event body; use the live API body."

            class API:
                current = pr
                after = None
                records = [approval(sha=head)]
                reads = 0

                def pull(self, number):
                    self.reads += 1
                    return self.after if self.reads > 1 and self.after is not None else self.current

                def reviews(self, number):
                    return self.records

                def permission(self, user):
                    return "write"

            result = gate.run_gate(root, event, POLICY, API())
            self.assertFalse(result["errors"])
            self.assertEqual(result["counted"]["added"], 1)
            api = API()
            api.records = []
            self.assertTrue(gate.run_gate(root, event, POLICY, api)["errors"])
            api = API()
            api.current = dict(pr, body="No required evidence")
            self.assertTrue(gate.run_gate(root, event, POLICY, api)["errors"])
            for field in ("head", "base"):
                api = API()
                api.after = copy.deepcopy(pr)
                api.after[field]["sha"] = "c" * 40
                with self.subTest(field=field), self.assertRaises(ValueError):
                    gate.run_gate(root, event, POLICY, api)
            stale = copy.deepcopy(event)
            stale["pull_request"]["head"]["sha"] = BASE
            with self.assertRaises(ValueError):
                gate.run_gate(root, stale, POLICY, API())
            wrong = copy.deepcopy(event)
            wrong["repository"]["full_name"] = "elsewhere/project"
            with self.assertRaises(ValueError):
                gate.run_gate(root, wrong, POLICY, API())

    def test_git_diff_uses_merge_base_instead_of_unrelated_base_changes(self):
        gate = load_gate()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()

            git("init", "-q")
            git("config", "user.name", "Test fixture")
            git("config", "user.email", "fixture@example.invalid")
            (root / "original.txt").write_text("base\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "Common ancestor")
            ancestor = git("rev-parse", "HEAD")
            (root / "base-only.txt").write_text("not in PR\n" * 20, encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "Base branch advance")
            base = git("rev-parse", "HEAD")
            git("checkout", "-qb", "topic", ancestor)
            (root / "head-only.txt").write_text("PR line\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "PR change")
            head = git("rev-parse", "HEAD")
            total, counted = gate.diff_stats(gate.git_diff(root, base, head), [])
            self.assertEqual(total, {"added": 1, "deleted": 0, "net_growth": 1, "binary_files": 0})
            self.assertEqual(counted, total)


if __name__ == "__main__":
    unittest.main()
