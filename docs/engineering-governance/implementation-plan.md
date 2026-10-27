# Governance baseline implementation plan

**Goal:** implement the owner's GOV-001 through GOV-010 policy without an
application framework, a default-branch push, or fabricated enforcement claims.

**Baseline (2026-10-27):** private repository, zero commits and branches, configured
default `main`; admin access verified. Protection/rules APIs return HTTP 403 with
a plan-upgrade requirement. Only RaviiTF is a collaborator. The owner selected
VidhiTF for security ownership; that account currently has no repository access.
Default Actions token is already read-only and cannot approve PRs.

**Design:** standard-library Python checks plus actionlint and Gitleaks; no runtime
dependencies. Native GitHub review rules remain essential. A custom approval bot
would be weaker and is rejected. No application scaffold or placeholder build is
appropriate in an empty repository. Local feature-branch preparation is authorized;
initializing remote `main` is a separate owner decision because a PR needs a base.

## Tasks and evidence

- [x] Implement PR metadata validation through `scripts/governance.py pr EVENT`.
  First demonstrate rejection of an empty PR; then test complete evidence,
  placeholders, hidden comments, fenced headings, malformed events and literal
  untrusted input. Validate structure only; never attest that a claimed test ran.
- [x] Implement `scripts/governance.py repository [ROOT]`: reject forbidden
  credential filenames and whitespace defects in versioned/submittable text.
  Exercise real temporary Git repositories, including force-added ignored files.
- [x] Add instructions, practical PR template, ownership and nonduplicative
  contribution/security/governance policies. Cover every mission requirement.
- [x] Add read-only Actions workflows for governance tests/hygiene, workflow lint,
  full-history and working-tree secret detection, and PR metadata from base code.
  Pin action SHAs and binary hashes. Add weekly GitHub Actions dependency updates.
- [x] Run tests, both validators, scanner positive/negative controls, and independent
  adversarial review; fix confirmed findings and rerun integrated verification.
- [x] Inspect/enable supported remote controls; record exact blockers and a
  protection payload/checklist. Do not require checks before successful remote runs.

## Review focus

Untrusted PR content must stay data; an author must not replace the base metadata
validator. Missing/null/malformed events must fail closed. Ignored credential files
that are force-added must be detected. Secret scanning must cover uncommitted files
and history without printing secret values. Missing branches, plan restrictions,
and unavailable reviewers must never be presented as active merge protection.

Execution is inline with a bounded independent reviewer at the end, as requested
by the standing workflow. No user changes existed. No worktree can be based on an
empty Git history; use the fresh clone's orphan feature branch instead.
