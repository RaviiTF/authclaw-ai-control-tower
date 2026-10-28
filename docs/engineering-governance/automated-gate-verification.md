# Automated Governance Gate verification — 2026-10-28

## Scope and baseline

Local branch `governance/automated-gate` starts from merged main
`30f2a5a10a1979fd3ebc8a9b09a6ba1fc13ebe1a`. The working tree was clean before
implementation. PR #1 was approved by VidhiTF and merged outside this task.
Dependabot branches were preserved. No commit, push, PR creation, merge, rule,
visibility, plan or collaborator change was performed by this implementation.

## Files changed

Added scripts/governance_gate.py, tests/test_governance_gate.py,
.github/governance-policy.json, .github/workflows/governance-gate.yml and the
automated-gate design/operation and verification documents in this directory.
Updated evidence-policy.md and testing-policy.md to explain the new checks.
The existing disclosure parser and four required workflows/job names are preserved.
No production application, architecture or dependencies were introduced.
Final local Git diff: 730 additions, zero deletions, 730 net lines; within the
configured 1,000-added/750-net budgets, with zero binary files or exclusions.

## Implemented behavior

Live read-only GitHub API records supply PR body, reviews and current reviewer
permissions. Approval requires an allowlisted human other than author/owner,
write-level access and the exact head SHA. Later decisive reviews invalidate older
approval; comments alone do not. Missing evidence, unauthorized/stale/no approval,
closed PR, malformed data, API errors and changed snapshots fail closed.

Git three-dot numstat supplies additions/deletions/net growth and binary counts,
including renames. Configurable initial caps are 1,000 additions, 750 net lines,
zero binary files; exclusions are empty. Both sides of a rename must match any
explicit exclusion. Deletions cannot hide excessive additions. No body approval
marker or author-supplied LOC count satisfies the gate.

## Checks and actual results

- Standard-library suite: **31 tests passed**, including all original 15 tests.
- Real temporary Git repositories prove additions, renames, merge-base semantics
  and orchestration. Cases cover no approval, invalid identity/access, stale or
  dismissed approval, excessive growth, missing evidence and malformed records.
- actionlint 1.7.12, repository hygiene and diff whitespace validation passed.
- Gitleaks 8.30.1 file/history preflight found no secrets; final file scan passed.
- Independent adversarial review reran all 31 tests and found no material defect.
- Live read-only adapter probe verified PR #1's actual VidhiTF approval at head
  82baae7 and current write access; closed PR was rejected as a current gate pass.
- Full CLI against open PR #2 fetched real Git objects: 2 additions, 2 deletions,
  zero net growth. It returned expected exit **1** for missing evidence/approval.
  Neither PR nor any review/description was modified by these probes.

New hosted Governance Gate CI: **NOT RUN — changes are local and unpublished**.
Existing PR #1's four baseline checks passed; those are not results for this gate.
Actual Actions-token metadata access and review-event ordering remain unverified.

## Effective GitHub settings and remaining blockers

Read-only inspection confirmed the repository is public and main is protected by
active ruleset 25955410: PRs, one code-owner approval, stale dismissal, latest-push
approval, resolved conversations, strict required checks, no force/deletion and
no bypass actors. Required contexts remain Governance tests and hygiene, Workflow
lint, Secret scan and PR disclosure, bound to GitHub Actions app 15368.

The new Governance Gate context is **not required or published**. No claim is made
that its future failure currently blocks merging. Publication needs authorization;
reviewed base installation and a subsequent actual successful run are prerequisites
to requiring it. First installation fails closed while base code/policy is absent;
there is no execution of untrusted head code or false bootstrap pass.

Base-pinned scripts do not protect a PR-editable workflow file by themselves;
native CODEOWNER review must guard that file. REST reads are not an atomic lock;
native merge-time review/pusher/thread rules remain essential. A real human
approval/reapproval cycle and malicious head execution were not fabricated as tests.
The repository stays public on GitHub Free under the owner's current decision.
