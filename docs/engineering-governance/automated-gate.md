# Automated Governance Gate: design and implementation plan

Baseline: 2026-10-28, clean checkout from merged main `30f2a5a`; public GitHub Free,
VidhiTF has write access, native ruleset 25955410 requires PRs, one code-owner
approval, fresh/latest-push review, resolved conversations and four passing checks.
No publication, merge, access, plan or visibility change is authorized by this task.

## Design

Reuse the existing disclosure parser. Add a standard-library Python gate and a
JSON policy defining the repository, authorized reviewers and growth limits.
Initial limits: 1,000 added lines, 750 net new lines, zero binary files, no path
exclusions. The earlier PR-size bands remain human review guidance; these are
explicit automated budgets, configurable through a separately reviewed policy PR.

Use Git's base...head numstat, including deletions and rename handling, rather than
PR-description counts. Report both full and policy-counted additions/deletions.
Exclusions require both sides of a rename to match, and are never implicit for
lockfiles, generated files or migrations. Binary changes need an explicit budget.

Fetch actual PR/review/permission records through read-only `gh api`. A qualifying
approval must be by an allowlisted human with current write/maintain/admin access,
excluding PR author and repository owner, at the exact current head SHA. Later
changes-requested/dismissed decisions invalidate approval; comments alone do not.
Reject malformed, stale, wrong-repository or mismatched event/PR data. Recheck the
live PR before success. Never trust approval markers in the body or print secrets.

Run on PR metadata/commit events and review submitted/edited/dismissed events.
Checkout only trusted base code/policy, fetch PR Git objects as data, and never
execute head code. Use read-only contents/pull-requests permissions, existing pinned
actions and a bounded timeout. Native rules remain authoritative for actual pusher
identity, merge-time races and conversation resolution; the gate is not a bypass.

## Implementation sequence

- [x] Add failing tests for actual-review decisions, authorization, freshness,
  missing evidence, configurable limits, real Git changes/renames and API errors.
- [x] Implement gate policy/review/numstat validation and live GitHub CLI adapter.
- [x] Add fail-closed trusted-base workflow, recheck review changes and preserve
  existing required check names.
- [x] Document activation, limits, exclusions, evidence and remaining trust limits.
- [x] Run focused/full tests, actionlint, file/history scans and independent review;
  fix confirmed findings, simplify safely and rerun integrated verification.

## Activation boundary

The new **Governance Gate** job is not published or required yet. Installing its
code/policy on main requires an authorized, natively reviewed PR using the current
four required checks. Before that reviewed installation reaches the base, the
new base-code job fails closed because the module/policy is absent; there is no
untrusted-head fallback or false bootstrap success. Do not require the new context
until a subsequent PR produces a successful actual run. Publishing, merging and
changing required contexts require their own existing authorization to apply.

## Policy and operation

`authorized_reviewers` is an explicit allowlist, initially the previously authorized
VidhiTF. The gate also verifies current access through GitHub's permission API;
allowlist membership alone is insufficient. Keep policy and CODEOWNERS aligned by
reviewed changes. The author, repository owner and bots cannot satisfy this gate.
An unavailable API or malformed record does not become approval evidence.

Git totals are reported independently of policy-counted totals. Exclusion patterns
are case-sensitive Python fnmatch globs over repository-relative forward-slash
paths, not gitignore syntax. A rename is excluded only when both names match an
explicit exclusion. Net growth is additions minus deletions; the independent
addition cap prevents hiding a large addition behind unrelated deletions. Binary
files count separately because Git cannot measure their textual LOC. No broad
exclude-all pattern is accepted. Policy changes take effect for subsequent PRs
after reaching their reviewed base, not for the PR proposing the policy change.

The CLI consumes the real event, reads the current PR body rather than stale event
text, validates repository/base/head identity, fetches the PR ref as Git data and
checks its fetched SHA. It loads all paginated reviews, uses the latest decisive
review per person, and verifies current write-level access. Approval must refer to
the exact head commit. It rechecks PR identity/body before returning success and
does not accept a changed snapshot. Read-only REST calls cannot atomically lock a
PR/review/permission snapshot; native merge-time rules remain essential. In
particular the gate does not infer the actual last pusher from a commit author.

The `gh` CLI must be installed (present on the configured GitHub-hosted Ubuntu
runner). It uses the existing authenticated CLI locally or the step-scoped
read-only GH_TOKEN in Actions. No PAT collection, write token, new dependency,
checkout credential persistence or PR-head execution is introduced. Logs contain
metrics, approved identities and safe diagnostics, not body text/API errors/tokens.
