# Testing policy

Current stack: Git, Python 3.14 standard library, Markdown and GitHub Actions YAML.
No application stack, package dependencies, database or build exists. Application
lint/type checks, unit/integration/E2E tests, builds, package audit/lock consistency
and migrations are not applicable yet; no passing placeholder jobs are supplied.
Before adding a stack, add its real documented install, frozen-lock, lint, type,
tests, build, vulnerability and relevant integration/migration commands to CI.

Run from the repository root:

```text
python -m unittest discover -s tests -v
python scripts/governance.py repository
actionlint -shellcheck= -pyflakes=
gitleaks dir --no-banner --redact=100 .
gitleaks git --no-banner --redact=100 --log-opts=--all .
```

Use actionlint 1.7.12 and Gitleaks 8.30.1. Workflow downloads pin version and SHA-256;
action references pin immutable commits. Optional ShellCheck/Pyflakes integrations
are disabled explicitly, so actionlint verifies Actions syntax/expressions, not
general Bash/Python static analysis. Review these binary pins for updates manually;
weekly Dependabot PRs cover action references, not embedded binary versions.
Standard-library Python has no third-party lockfile to audit.

`Governance tests and hygiene` runs real validator tests plus whitespace and
credential-filename checks over Git's tracked and nonignored candidate files.
It catches force-added ignored credential files. It does not inspect secret values;
`Secret scan` uses Gitleaks defaults over full reachable fetched history and files.
Do not add scan allowlists to hide genuine findings. Verify scanner changes with
safe synthetic positive/negative fixtures and ensure values remain redacted.
History scanning is blocked before the first commit; directory scanning still works.

`Workflow lint` validates every workflow. `PR disclosure` validates the actual PR
event with trusted base code using a read-only token, no secrets and no PR-head
execution. It reruns on body edits and new commits. There are no path filters or
continue-on-error gates. Quality CI runs on main pushes and relevant PRs; body
edits rerun only disclosure validation to avoid duplicating quality jobs. Required status
contexts must be observed in successful GitHub PR runs before activation.

Test changes through public interfaces and real collaborators where practical.
Reproduce failures, make a focused fix, retest adjacent behavior and re-review.
After safe simplification, rerun affected checks. Use an independent review before
final integrated verification. Disclose unavailable tools, environment failures and
all unverified runtime paths; follow evidence-policy.md.

On this Windows sandbox, Python's default temp directory was inaccessible. For local
tests set TEMP and TMP to a writable scratch directory outside the tracked tree.
This is an execution-environment workaround, not an application change.

The prospective `Governance Gate` uses `scripts/governance_gate.py` and
`.github/governance-policy.json`. Its tests run in the same standard-library suite.
For a real PR event, run `python scripts/governance_gate.py --event EVENT.json
--fetch` from a trusted checkout with authenticated read-only `gh` access. This
reads API records and fetches Git objects; it does not publish or approve anything.
API/permission errors fail closed. It requires an open PR, full SHAs and a matching
repository. A local historical review probe is not a hosted gate run.

The new workflow runs for PR changes and review submission/edit/dismissal, with
per-PR cancellation of obsolete runs. No PR head code is executed with its token.
Its code/policy must already exist on the reviewed base; first-install and required
context activation are explicitly described in automated-gate.md. The existing
four required contexts are preserved. Do not claim the new context is enforced
until a real successful run is observed and native rules are deliberately updated.
