# Repository rules and activation

Latest inspection: 2026-10-27, `RaviiTF/authclaw-ai-control-tower`, public, authenticated
RaviiTF admin. The owner explicitly authorized the one-time three-file seed and
governance PR. The configured default `main` now exists at
`df5237cb2dc66da7b14fb6b8c2e81893b62c12e1`. No existing work was overwritten.
The feature branch descends from the seed, not the earlier orphan history. Original
preparation bytes were verified before aligning that checkout to published history.

## Verified remote state

- The previous private-repository inspection returned HTTP 403 requiring a plan
  upgrade for protection/rules APIs. At the latest execution's start the repository
  was already public; this agent did not change visibility. Rulesets now return
  HTTP 200. Ruleset 25955410, **Main governance**, is now active
  for `refs/heads/main`, with no bypass actors. Effective-rule readback confirms
  no deletion, no non-fast-forward pushes and four required checks from app 15368,
  with strict up-to-date validation. Its `pull_request` rule now requires **1**
  approval, code-owner review, latest-push approval and resolved conversations;
  approvals are dismissed on new pushes. There are no bypass actors.
- VidhiTF accepted authorized invitation 339959336 and has verified `write`
  permission. The invitation list and CODEOWNERS error list are both empty.
  RaviiTF is the author/admin and does not count as independent review.
- Actions is enabled. Default token permission is `read` and
  `can_approve_pull_request_reviews` is `false`; these already matched policy.
- Dependency vulnerability alerts were disabled (GET returned 404), then enabled
  using PUT `/vulnerability-alerts`; a subsequent GET returned 204. There is no
  dependency manifest yet, so this does not demonstrate a dependency audit.
- Hosted PR runs 40502040013 (Governance) and 40502040015 (PR evidence) passed at
  `be68fa98618bab18722d51ff2956b5c96f5782a4`. All four exact check contexts and
  GitHub Actions app 15368 were observed before making those checks required.
  The latest-head results must also be verified after further commits.
- After full review activation, PR #1 reports `reviewDecision: REVIEW_REQUIRED`
  and `mergeStateStatus: BLOCKED`. It remains open and unmerged. This is actual
  native review enforcement, not an inference from local files or CI success.

## Required administrator sequence

1. Follow the reviewed preflight and bootstrap plan in bootstrap-preflight.md.
   The mission permits preparing temporary public operation, but any visibility
   mutation needs explicit authorization. The repository is already public.
   Do not toggle visibility repeatedly. Before restoring private visibility,
   confirm a plan supporting private protection and read back rules afterward.
   This task does not authorize purchasing a plan.
2. Accepted write access and valid CODEOWNERS were verified before review rules
   were activated, as authorized by the owner. Reverify eligibility if permissions
   change. CODEOWNERS contains only VidhiTF; do not add arbitrary reviewers or
   count the owner as independent review.
3. The explicitly authorized initial base now contains exactly README.md, the
   trusted disclosure validator and CODEOWNERS. See bootstrap-preflight.md for the
   seed SHA and audit receipt. This is a one-time exception, not authorization for
   further default-branch pushes. Publish remaining changes only through the PR.
4. [PR #1](https://github.com/RaviiTF/authclaw-ai-control-tower/pull/1) is open from
   the authorized feature branch, descending from the seed. All four jobs have
   actual successful PR runs, including trusted base-code disclosure. Quality CI
   now avoids duplicate feature-push runs; PR-body edits rerun disclosure only.
5. Preserve active ruleset 25955410. All native PR/review requirements above were
   applied only after accepted write access and successful check contexts were
   verified. Keep owner administrative recovery for explicit audited decisions;
   no routine bypass is configured. Do not weaken rules to get a merge through.
6. Required contexts are **Governance tests and hygiene**, **Workflow lint**,
   **Secret scan**, **PR disclosure**, bound to verified app 15368. The local
   `branch-protection.json` remains a classic-API reference; that payload itself
   was not applied. Equivalent full policy is already active through the ruleset;
   do not blindly add duplicate classic protection or replace stronger settings.
7. Recheck `/rulesets/25955410` and `/rules/branches/main` after rule/permission or
   visibility changes. A controlled missing-evidence PR edit produced a failed
   required check and `BLOCKED`; restoration passed. Review-required blocking was
   also observed after activation. Stale/latest-push/thread rules are verified in
   effective configuration; a real human approval/reapproval cycle has not yet
   been exercised. Do not impersonate review or attempt destructive push tests.

## Repository-file controls

AGENTS.md and CONTRIBUTING.md define GOV-001/002/005/006/007; the PR template and
base metadata validator cover GOV-004/005 disclosure structure. Read-only,
SHA/hash-pinned CI and real tests cover the currently applicable GOV-003 checks.
CODEOWNERS covers every path; security-review-policy.md addresses GOV-008.
Credential ignores, filename guard, Gitleaks and dependency-update guidance cover
GOV-009. GOV-010 policies link to each other without pretending to be remote rules.
Native GitHub requirements are still necessary to make CI and code ownership
mandatory. A malicious PR can propose weakening its own workflows; code-owner
review and protected base rules must reject that change.

Secrets push protection, private vulnerability reporting and advanced-security
features are not assumed enabled. Confirm supported features in Settings > Code
security and enable those available under the owner's approved plan. Do not buy
services or assume GitHub native scanning merely because the CI scanner exists.

GitHub's [visibility documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
warns that features can become unavailable after restoring privacy. Its
[ruleset documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
limits private-repository rulesets to supported paid plans. Public configuration
is not proof of private enforcement. Restoration requires explicit authorization,
remote files, effective rules, eligible review and successful CI as specified by
the mission; report any capability lost rather than silently weakening governance.
