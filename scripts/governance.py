"""Check PR disclosure structure and repository hygiene; never attest test claims."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


SECTIONS = ("Summary", "Problem", "Scope", "Approach", "Evidence", "Security impact",
            "Compatibility", "Database and migrations", "Risks and limitations",
            "Rollback", "Instructions and quality checks")
OUTCOMES = ("Passed", "Failed", "Not run", "Blocked", "Static inspection", "Integration/E2E")


def meaningful(value):
    for line in value.splitlines():
        line = line.strip().strip("-* \t")
        if (line and not re.fullmatch(r"\[[ xX]?\]", line) and
                not re.match(r"^(TODO|TBD|<)", line, re.IGNORECASE) and
                not re.match(r"^(N/?A|None)\W*$", line, re.IGNORECASE)):
            return True
    return False


def validate_pr(body):
    if not isinstance(body, str):
        return ["PR body must be text."]
    body = re.sub(r"<!--.*?(?:-->|$)", "", body, flags=re.DOTALL)
    sections, current, fence = {}, None, None
    for line in body.splitlines():
        delimiter = re.match(r"^\s*(`{3,}|~{3,})", line)
        if delimiter:
            token = delimiter[1]
            if fence is None:
                fence = token
            elif (token[0] == fence[0] and len(token) >= len(fence) and
                  not line[delimiter.end():].strip()):
                fence = None
            continue
        if fence:
            continue
        if line.startswith("## "):
            current = line[3:].strip().casefold()
            sections.setdefault(current, [])
        elif current:
            sections[current].append(line)
    errors = []
    for title in SECTIONS:
        lines = sections.get(title.casefold(), [])
        if not meaningful("\n".join(lines)):
            errors.append(f"Missing or unexplained section: {title}")
    evidence = "\n".join(sections.get("evidence", []))
    for label in OUTCOMES:
        match = re.search(rf"^[ \t]*(?:-[ \t]*)?{re.escape(label)}:[ \t]*(.*)$", evidence,
                          flags=re.MULTILINE | re.IGNORECASE)
        if not match or not meaningful(match[1]):
            errors.append(f"Evidence needs an explained outcome: {label}")
    return errors


def check_repository(root):
    result = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others",
                             "--exclude-standard", "-z"], capture_output=True)
    if result.returncode:
        return ["Cannot enumerate repository files with Git."]
    errors = []
    for name in sorted(set(result.stdout.decode("utf-8").split("\0")) - {""}):
        path = root / name
        if not path.exists():
            continue  # A staged removal has no working-tree content to validate.
        lower = path.name.lower()
        example = lower.endswith(".example")
        if not example and (lower == ".env" or lower.startswith(".env.") or
                            path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"} or
                            lower in {"credentials.json", "id_rsa", "id_ed25519"} or
                            name.lower().endswith(".aws/credentials")):
            errors.append(f"Forbidden credential filename: {name}")
        try:
            data = path.read_bytes()
            if b"\0" in data:
                continue
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if any(line.rstrip(" \t") != line for line in content.splitlines()):
            errors.append(f"Trailing whitespace: {name}")
        if content and not content.endswith("\n"):
            errors.append(f"Missing final newline: {name}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("pr").add_argument("event", type=Path)
    commands.add_parser("repository").add_argument("root", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    try:
        if args.command == "pr":
            event = json.loads(args.event.read_text(encoding="utf-8"))
            errors = validate_pr(event["pull_request"]["body"])
        else:
            errors = check_repository(args.root)
    except (OSError, ValueError, KeyError, TypeError):
        errors = ["Unable to validate input; expected readable repository files or a PR event JSON."]
    for error in errors:
        print(error)
    if not errors:
        print("Validation passed (structure only; test/security claims are not authenticated).")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
