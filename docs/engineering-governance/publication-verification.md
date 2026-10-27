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
Original uncommitted preparation files were preserved in the original checkout.

## 2. Commands and tests

Publication checkout: `D:/AI TOWER/.governance-publication`.
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

This is **partial governance**: mandatory PR, one-human-review, CODEOWNERS,
latest-push approval and conversation-resolution rules are **not active yet**.
An attempted interim PR rule with zero approvals was rejected by automatic
approval review because it left the independent-human-review policy unenforced;
it was not applied and no workaround was attempted. Full policy activation is
pending accepted reviewer access under the approved preflight. No claim is made
that the Merge button is disabled. Passing checks alone never authorize a merge.

## 7. Reviewer eligibility

Authorized invitation **339959336** was sent to VidhiTF with `write` permission;
it is pending acceptance. Current effective permission is public read. CODEOWNERS
API reports Unknown owner until qualifying access is accepted. RaviiTF is the
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

VidhiTF must accept qualifying write access. Then validate CODEOWNERS and activate
the full mandatory-review policy while preserving active safeguards. The full
prepared branch-protection.json has count 1, code-owner review, stale dismissal,
latest-push approval, conversation resolution, required checks, admin enforcement
and no force/deletion. It has not been applied. Confirm actual effective behavior
on an unmerged PR, without a destructive push/delete experiment.

Restoring private visibility requires a supported plan if protection is to remain
effective, completed mission prerequisites and explicit transition authorization.
Do not toggle visibility or remove rules to get a green result.

## 10. Local policy versus enforcement

Instructions, PR metadata requirements, tests and workflows are published in the
unmerged feature PR. Required CI and history safeguards are native/verified.
Mandatory independent approval and remaining PR rules are prepared/blocked, not
GitHub-enforced yet. All work remains unmerged; original preparation work is safe.
