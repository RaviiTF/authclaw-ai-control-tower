"""Fail closed on missing disclosure, excessive Git growth or unqualified reviews."""

import argparse
from datetime import datetime
import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from governance import validate_pr


SHA = re.compile(r"[0-9a-fA-F]{40}")
LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?")
LIMITS = ("max_added_lines", "max_net_growth_lines", "max_binary_files")


class GateError(ValueError):
    """A diagnostic safe to print without API response bodies or credentials."""


def validate_policy(policy):
    keys = {"repository", "authorized_reviewers", "excluded_paths", *LIMITS}
    if not isinstance(policy, dict) or set(policy) != keys:
        raise GateError("Policy has missing or unknown keys.")
    repository = policy["repository"]
    if (not isinstance(repository, str) or
            not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", repository) or
            repository.split("/")[1] in {".", ".."}):
        raise GateError("Policy repository must identify one GitHub repository.")
    for key in LIMITS:
        if type(policy[key]) is not int or policy[key] < 0:
            raise GateError("Policy limits must be nonnegative integers.")
    reviewers = policy["authorized_reviewers"]
    if (not isinstance(reviewers, list) or not reviewers or
            any(not isinstance(user, str) or not LOGIN.fullmatch(user) for user in reviewers) or
            len({user.casefold() for user in reviewers}) != len(reviewers)):
        raise GateError("Policy needs unique authorized human reviewer logins.")
    patterns = policy["excluded_paths"]
    if not isinstance(patterns, list) or any(
            not isinstance(pattern, str) or not pattern or
            pattern in {"*", "**", "**/*"} or pattern.startswith("/") or
            "\\" in pattern or "\0" in pattern or ".." in pattern.split("/")
            for pattern in patterns):
        raise GateError("Policy exclusions must be scoped relative glob patterns.")
    return policy


def pr_identity(pr, repository):
    try:
        number, author = pr["number"], pr["user"]["login"]
        head, base = pr["head"]["sha"], pr["base"]["sha"]
        actual_repository = pr["base"]["repo"]["full_name"]
        if (type(number) is not int or number < 1 or not isinstance(author, str) or
                not author or not isinstance(head, str) or not SHA.fullmatch(head) or
                not isinstance(base, str) or not SHA.fullmatch(base) or
                actual_repository.casefold() != repository.casefold()):
            raise GateError("PR identity, repository or revision is invalid.")
        return number, author.casefold(), base.lower(), head.lower()
    except (KeyError, TypeError, AttributeError):
        raise GateError("PR identity, repository or revision is invalid.") from None


def diff_stats(raw, patterns):
    if not isinstance(raw, bytes) or (raw and not raw.endswith(b"\0")):
        raise GateError("Git numstat is malformed.")
    records = raw.split(b"\0")[:-1]
    total = {"added": 0, "deleted": 0, "net_growth": 0, "binary_files": 0}
    counted, index = dict(total), 0
    while index < len(records):
        fields = records[index].split(b"\t", 2)
        index += 1
        if len(fields) != 3:
            raise GateError("Git numstat is malformed.")
        added, deleted, path = fields
        paths = [path]
        if not path:  # -z represents a rename as header NUL old NUL new NUL.
            paths = records[index:index + 2]
            index += 2
        if len(paths) != (1 if path else 2) or not all(paths):
            raise GateError("Git rename numstat is malformed.")
        if added == deleted == b"-":
            delta = {"added": 0, "deleted": 0, "binary_files": 1}
        elif added.isdigit() and deleted.isdigit():
            delta = {"added": int(added), "deleted": int(deleted), "binary_files": 0}
        else:
            raise GateError("Git numstat is malformed.")
        excluded = all(any(fnmatch.fnmatchcase(name.decode("utf-8", "surrogateescape"), pattern)
                           for pattern in patterns) for name in paths)
        for key, value in delta.items():
            total[key] += value
            if not excluded:
                counted[key] += value
    for stats in (total, counted):
        stats["net_growth"] = stats["added"] - stats["deleted"]
    return total, counted


def qualified_reviews(reviews, permissions, policy, author, head):
    if not isinstance(reviews, list) or not isinstance(permissions, dict):
        raise GateError("GitHub review or permission records are malformed.")
    latest = {}
    for review in reviews:
        try:
            state = review["state"]
            if state == "PENDING":
                continue
            login, kind = review["user"]["login"], review["user"]["type"]
            identifier, commit = review["id"], review["commit_id"]
            submitted = datetime.fromisoformat(review["submitted_at"])
            if (state not in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED", "COMMENTED"} or
                    not isinstance(login, str) or not login or type(identifier) is not int or
                    identifier < 1 or not isinstance(commit, str) or not SHA.fullmatch(commit) or
                    submitted.tzinfo is None):
                raise GateError("GitHub review records are malformed.")
            if state == "COMMENTED":
                continue
            key = login.casefold()
            if key not in latest or (submitted, identifier) > latest[key][0]:
                latest[key] = ((submitted, identifier), state, commit.lower(), kind)
        except (KeyError, TypeError, AttributeError, ValueError):
            raise GateError("GitHub review records are malformed.") from None
    allowed = {user.casefold() for user in policy["authorized_reviewers"]}
    forbidden = {author, policy["repository"].split("/")[0].casefold()}
    permissions = {user.casefold(): level for user, level in permissions.items()}
    return sorted(user for user, (_, state, commit, kind) in latest.items()
                  if user in allowed - forbidden and kind == "User" and state == "APPROVED"
                  and commit == head and permissions.get(user) in {"write", "maintain", "admin"})


def evaluate(pr, reviews, permissions, numstat, policy):
    validate_policy(policy)
    _, author, _, head = pr_identity(pr, policy["repository"])
    errors = validate_pr(pr.get("body"))
    if pr.get("state") != "open":
        errors.append("Governance Gate requires an open PR.")
    total, counted = diff_stats(numstat, policy["excluded_paths"])
    for metric, limit in (("added", "max_added_lines"), ("net_growth", "max_net_growth_lines"),
                          ("binary_files", "max_binary_files")):
        if counted[metric] > policy[limit]:
            errors.append(f"Git {metric} {counted[metric]} exceeds policy limit {policy[limit]}.")
    try:
        approved = qualified_reviews(reviews, permissions, policy, author, head)
    except GateError:
        errors.append("GitHub review records are malformed.")
        approved = []
    if not approved:
        errors.append("Missing authorized independent human approval for the current head SHA.")
    return {"head": head, "total": total, "counted": counted,
            "approved_by": approved, "errors": errors}


class GitHub:
    def __init__(self, repository):
        self.repository = repository

    def api(self, suffix, paginated=False):
        args = ["gh", "api", "--hostname", "github.com", "--method", "GET",
                "-H", "Accept: application/vnd.github+json",
                "-H", "X-GitHub-Api-Version: 2022-11-28"]
        if paginated:
            args += ["--paginate", "--slurp"]
        args.append(f"repos/{self.repository}/{suffix}")
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=45,
                                    env={**os.environ, "GH_PROMPT_DISABLED": "1"})
            if result.returncode:
                raise GateError("GitHub API request failed; approval evidence is unavailable.")
            return json.loads(result.stdout)
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
            raise GateError("GitHub API evidence is unavailable or malformed.") from None

    def pull(self, number):
        return self.api(f"pulls/{number}")

    def reviews(self, number):
        pages = self.api(f"pulls/{number}/reviews?per_page=100", paginated=True)
        if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
            raise GateError("GitHub API review pagination is malformed.")
        return [review for page in pages for review in page]

    def permission(self, user):
        data = self.api(f"collaborators/{user}/permission")
        if not isinstance(data, dict) or not isinstance(data.get("user"), dict) or \
                data["user"].get("login", "").casefold() != user.casefold() or \
                data.get("permission") not in {"none", "read", "write", "maintain", "admin"}:
            raise GateError("GitHub API reviewer permission is malformed.")
        return data["permission"]


def git_command(root, *args):
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        raise GateError("Git diff evidence is unavailable.") from None
    if result.returncode:
        raise GateError("Git evidence failed; ensure both PR revisions and their merge base exist.")
    return result.stdout


def git_diff(root, base, head):
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise GateError("Git revisions must be full commit SHAs.")
    return git_command(root, "diff", "--numstat", "-z", "--find-renames", "--no-ext-diff",
                       "--no-textconv", f"{base}...{head}", "--")


def run_gate(root, event, policy, github, fetch=False):
    validate_policy(policy)
    try:
        expected = pr_identity(event["pull_request"], policy["repository"])
        if event["repository"]["full_name"].casefold() != policy["repository"].casefold():
            raise GateError("Event belongs to another repository.")
    except (KeyError, TypeError, AttributeError):
        raise GateError("A matching pull request event is required.") from None
    number = expected[0]
    pr = github.pull(number)
    if pr_identity(pr, policy["repository"]) != expected:
        raise GateError("Event is stale or does not match the live PR.")
    if fetch:
        git_command(root, "fetch", "--no-tags", "--no-recurse-submodules", "origin",
                    f"refs/pull/{number}/head")
        if git_command(root, "rev-parse", "FETCH_HEAD").decode().strip().lower() != expected[3]:
            raise GateError("PR head changed during Git fetch; rerun against the current head.")
    reviews = github.reviews(number)
    permissions = {user: github.permission(user) for user in policy["authorized_reviewers"]}
    result = evaluate(pr, reviews, permissions, git_diff(root, expected[2], expected[3]), policy)
    latest = github.pull(number)
    if pr_identity(latest, policy["repository"]) != expected or latest.get("body") != pr.get("body"):
        raise GateError("PR changed during validation; rerun against the current PR.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True, type=Path)
    parser.add_argument("--policy", type=Path, default=Path(".github/governance-policy.json"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    try:
        policy = validate_policy(json.loads(args.policy.read_text(encoding="utf-8")))
        event = json.loads(args.event.read_text(encoding="utf-8"))
        result = run_gate(args.root, event, policy, GitHub(policy["repository"]), args.fetch)
        print(json.dumps(result, sort_keys=True))
        return bool(result["errors"])
    except GateError as error:
        print(f"Governance Gate failed: {error}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        print("Governance Gate failed: input or evidence is unavailable or malformed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
