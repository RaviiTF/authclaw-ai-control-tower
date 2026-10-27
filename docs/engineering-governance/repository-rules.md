# Repository rules and activation

Latest inspection: 2026-10-27, `RaviiTF/authclaw-ai-control-tower`, public, authenticated
RaviiTF admin. The owner explicitly authorized the one-time three-file seed and
governance PR. The configured default `main` now exists at
`df5237cb2dc66da7b14fb6b8c2e81893b62c12e1`. No existing work was overwritten.
The preserved preparation tree remains separate from the publication checkout;
the feature branch descends from the seed, not the earlier orphan history.

## Verified remote state

- The previous private-repository inspection returned HTTP 403 requiring a plan
  upgrade for protection/rules APIs. At the latest execution's start the repository
  was already public; this agent did not change visibility. Rulesets now return
  HTTP 200 with `[]`. After the authorized seed, main's branch metadata reports
  `protected: false`. No effective merge protection is claimed yet.
- Only RaviiTF is a collaborator. VidhiTF is a real account selected by the owner
  for security review. Its write invitation was authorized and sent (339959336);
  current effective permission remains public `read` pending acceptance.
- Actions is enabled. Default token permission is `read` and
  `can_approve_pull_request_reviews` is `false`; these already matched policy.
- Dependency vulnerability alerts were disabled (GET returned 404), then enabled
  using PUT `/vulnerability-alerts`; a subsequent GET returned 204. There is no
  dependency manifest yet, so this does not demonstrate a dependency audit.
- No hosted workflow/check run has been verified. The files in this branch do
  not yet enforce PRs, required reviews, CI or merge blocking on GitHub.

## Required administrator sequence

1. Follow the reviewed preflight and bootstrap plan in bootstrap-preflight.md.
   The mission permits preparing temporary public operation, but any visibility
   mutation needs explicit authorization. The repository is already public.
   Do not toggle visibility repeatedly. Before restoring private visibility,
   confirm a plan supporting private protection and read back rules afterward.
   This task does not authorize purchasing a plan.
2. The owner authorized VidhiTF's write invitation and it has been sent. Verify
   accepted write access before configuring mandatory code-owner review.
   The repository owner cannot count as the
   independent reviewer; CODEOWNERS contains only VidhiTF. Do not add arbitrary
   reviewers or configure mandatory ownership into a knowingly unmergeable state.
3. The explicitly authorized initial base now contains exactly README.md, the
   trusted disclosure validator and CODEOWNERS. See bootstrap-preflight.md for the
   seed SHA and audit receipt. This is a one-time exception, not authorization for
   further default-branch pushes. Publish remaining changes only through the PR.
4. Publish through the owner's authorized feature-branch/PR bootstrap process;
   run workflows, inspect actual check-run names, head SHA, conclusions and GitHub
   Actions app ID. First run the metadata workflow on a subsequent PR with base
   tooling present. Do not mark nonexistent or failing checks as required.
5. Inspect existing protection/rulesets again; preserve stronger controls. In
   Settings > Branches add/edit protection for the actual default branch `main`:
   require PRs, **1 approval**, stale-approval dismissal, code-owner review, latest
   reviewable-push approval, conversation resolution and passing checks with the
   branch up to date. Disable force pushes/deletion. Apply rules to admins; do not
   add ordinary bypass actors. Keep owner admin access for exceptional recovery;
   recovery changes must be explicit, audited owner decisions, never agent bypasses.
6. Candidate job contexts are **Governance tests and hygiene**, **Workflow lint**,
   **Secret scan**, **PR disclosure**. They are explicit unique job names in the
   two workflows. The supplied `branch-protection.json` is a proposed REST payload,
   **not applied**. Verify observed contexts and app ID before using it. App ID
   15368 was verified via GET `/apps/github-actions`; also confirm it on real runs.
   Never blindly replace a stronger existing configuration with this baseline.
7. After the prerequisites above and reconciliation with existing rules, an admin
   may apply the reviewed payload from the repo root:

   ```text
   gh api --method PUT repos/RaviiTF/authclaw-ai-control-tower/branches/main/protection --input docs/engineering-governance/branch-protection.json
   ```

8. Read back `/branches/main/protection`, `/rulesets` and `/rules/branches/main`.
   Verify effective requirements and native approval behavior on an unmerged PR:
   author approval cannot count; a bot run cannot count as a human approval; failed
   or missing checks block merge; new commits dismiss approvals and require fresh
   latest-push approval; unresolved threads block merge. Verify force-push/deletion
   prohibitions via configuration without attempting destructive operations.
   Record evidence rather than claiming the Merge button is disabled from files.

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
