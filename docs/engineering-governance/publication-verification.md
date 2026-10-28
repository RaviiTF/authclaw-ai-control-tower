# Publication and remote verification

2026-10-27 (Asia/Calcutta). This supersedes the historical preflight for current
publication status; the original preflight remains as an audit record.

## 1. Changes made

The owner explicitly authorized the exact three-file initial seed, feature-branch
publication/unmerged PR and VidhiTF write invitation. Seed commit
`df5237cb2dc66da7b14fb6b8c2e81893b62c12e1` contains exactly README.md,
scripts/governance.py and .github/CODEOWNERS (136 lines). It was scanned and pushed
without force or bypass. No other default-branch push occurred.

The feature descends from that seed and proposes the remaining governance baseline
through PR #1. A small workflow correction eliminates duplicate feature push/PR
quality jobs and reruns disclosure alone for PR-body edits. Base parser, README and
CODEOWNERS are unchanged. No application behavior or runtime dependency changed.
Original preparation bytes were preserved, verified against the audited snapshot,
then safely aligned to the published branch. The canonical checkout is now
`D:/AI TOWER/authclaw-ai-control-tower`.

## 2. Commands and tests

Initial publication checkout: `D:/AI TOWER/.governance-publication`; subsequent
verification/PR updates use the canonical checkout above.
Ran `python -m unittest discover -s tests -v` (15 passed),
`python scripts/governance.py repository` (passed), actionlint 1.7.12 (passed),
Gitleaks 8.30.1 directory/history scans (passed), staged/diff whitespace checks
(passed) and PR-body validation (passed). TEMP/TMP use writable workspace scratch.
Only reviewed Git candidates were copied; ignored bytecode and external tooling
were excluded. Noreply commit identity is local to the publication checkout.

## 3. Actual CI results

Successful PR runs at `be68fa98618bab18722d51ff2956b5c96f5782a4`:

- [Governance 40502040013](https://github.com/RaviiTF/authclaw-ai-control-tower/actions/runs/40502040013):
  Governance tests and hygiene, Workflow lint, Secret scan all successful.
- [PR evidence 40502040015](https://github.com/RaviiTF/authclaw-ai-control-tower/actions/runs/40502040015):
  PR disclosure successful using the seed's base validator.

Check-run API confirmed exact names, head SHA, `success` conclusions and app ID
15368. Those observed contexts were then made required. Final documentation commits
require fresh latest-head runs; do not infer those results from older run links.
No fabricated build/type/database/deployment job exists for an absent application.

## 4. Visibility

Public before and after these operations. It was already public before this
execution; this agent made no visibility mutation. Publication while public was
explicitly authorized. Privacy restoration still needs its specified prerequisites
and explicit authorization, with effective-rule readback after the transition.
The earlier private state rejected protection APIs due to plan limits; public
configuration cannot establish private protection. No plan was purchased.

## 5. Branch and PR

[PR #1](https://github.com/RaviiTF/authclaw-ai-control-tower/pull/1) is open and
unmerged: governance/engineering-baseline -> main. Main remains the exact approved
seed SHA. No human review, self/automatic approval, merge or force-push occurred.
The feature contains the initial connected baseline, tests and audit evidence;
its >500-line size is justified explicitly in the PR Scope.

## 6. Effective remote configuration

Ruleset **25955410 / Main governance** is active on `refs/heads/main` with
`bypass_actors: []`. Settings and effective branch-rules readback confirmed:

- `deletion` prohibition.
- `non_fast_forward` prohibition.
- `required_status_checks`: Governance tests and hygiene; Workflow lint; Secret
  scan; PR disclosure. All bound to integration 15368.
- `strict_required_status_checks_policy: true`; no create-time check exemption.
- `pull_request`: one approval, code-owner review, latest-push approval,
  stale-approval dismissal on pushes and resolved review threads.

The full review policy was activated after VidhiTF's accepted write access and
valid CODEOWNERS were verified. Effective branch-rules readback confirms all
parameters; PR #1 reports REVIEW_REQUIRED and BLOCKED. An earlier interim PR rule
with zero approvals was rejected by automatic
approval review because it left the independent-human-review policy unenforced;
it was not applied. The later full one-approval activation follows the approved
policy and the owner's conditional authorization. No merge was performed.

A live negative control removed the Blocked evidence category: run 40503094336
failed with exit 1 and GitHub reported BLOCKED. Restoring the complete body passed
in run 40503218116. These are actual CI-gate observations. No approval has yet been
submitted, so stale dismissal, reapproval and thread-resolution behavior are
configuration-verified, not demonstrated through a real human review cycle.

## 7. Reviewer eligibility

Authorized invitation **339959336** was accepted. Current effective permission is
`write`; the invitation list and CODEOWNERS error list are empty. RaviiTF is the
author/admin, not the independent reviewer. Do not request approval as a substitute
for access or count any bot/agent result as human review.

## 8. Security coverage

The complete publication candidate set was inspected and file-scanned. The seed's
one-commit history and subsequent feature history were scanned with full redaction
and no findings. Independent review scanned the first three published commits and
directory, reran 15 tests, hygiene, actionlint and whitespace checks, and found no
confirmed security/CI defect. Safe positive/negative scanner controls prove file
and deleted-file history detection. These are bounded checks, not a guarantee that
every secret type or future runtime vulnerability is absent. No production or
application integration behavior exists to verify. Final history must be rescanned
after documentation commits.

## 9. Remaining blockers

PR #1 awaits VidhiTF's actual qualifying review. Do not approve on another person's
behalf or merge without separate authorization. All configured native review rules
are active. The local branch-protection.json is an unapplied classic-API reference;
equivalent full enforcement is supplied by the active ruleset, with no bypass
actors. Do not duplicate or weaken it. A real human approval/reapproval cycle and
destructive force/delete experiments have not been performed.

Restoring private visibility requires a supported plan if protection is to remain
effective, completed mission prerequisites and explicit transition authorization.
Do not toggle visibility or remove rules to get a green result.

## 10. Local policy versus enforcement

Instructions, PR metadata requirements, tests and workflows are published in the
unmerged feature PR. Required CI and history safeguards are native/verified.
Mandatory independent approval, PR, code-owner, latest-push, stale-review and
conversation rules are now native/configuration-verified; review-required blocking
is observed on PR #1. All work remains unmerged, awaiting actual human review.
