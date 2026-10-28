import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "governance.py"
BODY = """## Summary
Document engineering controls.
## Problem
There are no contribution gates.
## Scope
Repository governance files only.
## Approach
Use native reviews and deterministic checks.
## Evidence
Passed: python -m unittest discover -s tests -v, exit 0.
Failed: None; all executed checks passed.
Not run: Application build; no application exists.
Blocked: Remote protection; current plan rejects it.
Static inspection: Reviewed Actions permissions.
Integration/E2E: Not run; no application exists.
## Security impact
Review gates are security-sensitive; no runtime boundary changes.
## Compatibility
N/A: no application interfaces exist.
## Database and migrations
N/A: no database exists.
## Risks and limitations
Native protection still needs a supported plan.
## Rollback
Revert this PR through another reviewed PR.
## Instructions and quality checks
Followed AGENTS.md and ran the checks listed above.
"""


class GovernanceTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True)

    def run_pr(self, body):
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory) / "event.json"
            event.write_text(json.dumps({"pull_request": {"body": body}}), encoding="utf-8")
            return self.run_cli("pr", event)

    def test_empty_pr_is_rejected(self):
        result = self.run_pr("")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Summary", result.stdout)

    def test_complete_pr_is_accepted_without_attesting_claims(self):
        result = self.run_pr(BODY)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("structure only", result.stdout)

    def test_every_missing_section_is_rejected(self):
        for heading in ("Summary", "Problem", "Scope", "Approach", "Evidence",
                        "Security impact", "Compatibility", "Database and migrations",
                        "Risks and limitations", "Rollback", "Instructions and quality checks"):
            with self.subTest(heading=heading):
                self.assertEqual(self.run_pr(BODY.replace("## " + heading, "## Other")).returncode, 1)

    def test_placeholders_hidden_comments_and_bare_na_do_not_count(self):
        for content in ("", "<!-- tests passed -->", "TODO", "TBD", "N/A", "<describe change>", "- [ ]"):
            with self.subTest(content=content):
                self.assertEqual(self.run_pr(BODY.replace("Document engineering controls.", content)).returncode, 1)

    def test_headings_inside_fences_do_not_supply_metadata(self):
        self.assertEqual(self.run_pr("```markdown\n" + BODY + "```\n").returncode, 1)

    def test_fence_with_trailing_text_does_not_end_code_block(self):
        self.assertEqual(self.run_pr("```markdown\n```still-fenced\n" + BODY + "```\n").returncode, 1)

    def test_multiple_empty_checkboxes_do_not_explain_a_section(self):
        self.assertEqual(self.run_pr(BODY.replace("Document engineering controls.", "- [ ]\n- [ ]")).returncode, 1)

    def test_empty_evidence_row_cannot_borrow_the_next_line(self):
        for label in ("Passed", "Failed", "Not run", "Blocked", "Static inspection", "Integration/E2E"):
            with self.subTest(label=label):
                lines = [label + ":" if line.startswith(label + ":") else line
                         for line in BODY.splitlines()]
                self.assertEqual(self.run_pr("\n".join(lines)).returncode, 1)

    def test_all_evidence_outcomes_need_an_explanation(self):
        for label in ("Passed", "Failed", "Not run", "Blocked", "Static inspection", "Integration/E2E"):
            with self.subTest(label=label):
                lines = [line for line in BODY.splitlines() if not line.startswith(label + ":")]
                self.assertEqual(self.run_pr("\n".join(lines)).returncode, 1)

    def test_null_and_wrong_type_body_are_rejected(self):
        for body in (None, {}, [], 123):
            self.assertEqual(self.run_pr(body).returncode, 1)

    def test_untrusted_content_is_neither_executed_nor_echoed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            payload = f"$(touch {marker}) SECRET_VALUE_DO_NOT_ECHO"
            result = self.run_pr(BODY.replace("Document engineering controls.", payload))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertNotIn(payload, result.stdout + result.stderr)

    def test_invalid_event_is_rejected_without_echoing_content(self):
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory) / "event.json"
            for value in ("SECRET_INVALID_JSON", "[]", "{}", '{"pull_request": null}'):
                event.write_text(value, encoding="utf-8")
                result = self.run_cli("pr", event)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertNotIn("SECRET_INVALID_JSON", result.stdout + result.stderr)

    def test_repository_hygiene_uses_git_and_detects_forced_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            (root / ".env").write_text("LOCAL_ONLY=example\n", encoding="utf-8")
            (root / "README.md").write_text("Clean text\n", encoding="utf-8")
            self.assertEqual(self.run_cli("repository", root).returncode, 0)
            subprocess.run(["git", "-C", str(root), "add", "-f", ".env"], check=True)
            result = self.run_cli("repository", root)
            self.assertEqual(result.returncode, 1)
            self.assertIn(".env", result.stdout)
            self.assertNotIn("LOCAL_ONLY", result.stdout)

    def test_repository_rejects_whitespace_and_allows_examples_and_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".env.example").write_text("URL=https://example.invalid\n", encoding="utf-8")
            (root / "image.bin").write_bytes(b"\x00\xff")
            self.assertEqual(self.run_cli("repository", root).returncode, 0)
            (root / "README.md").write_text("Bad whitespace \n", encoding="utf-8")
            self.assertEqual(self.run_cli("repository", root).returncode, 1)

    def test_repository_outside_git_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.run_cli("repository", directory).returncode, 1)


if __name__ == "__main__":
    unittest.main()
