# Contributing

Read AGENTS.md, SECURITY.md and the engineering-governance policies first.
Use a feature branch and a PR for every change, including governance files.
Never merge without at least one qualifying collaborator approval other than the
author, successful required checks and resolved review conversations. CI and AI
reviews do not replace human approval. Do not bypass controls or merge while an
eligible reviewer is unavailable. Changes after approval require fresh review.
The repository owner does not count as the independent reviewer. Do not invite
reviewers or change repository access without explicit authorization.

Keep one logical objective per PR. Preserve unrelated work and behavior. Prefer
existing functions and patterns; justify new dependencies and architecture changes.
Remove temporary debug code and unused code introduced by your change. Avoid
unrelated refactoring and artificial code compression. Never remove security checks
or meaningful tests to reduce size.

Size guidance: 1-100 substantive changed lines is small; 101-300 medium; 301-500
large and needs justification; above 500, split when practical or justify explicitly
in Scope. Account separately for generated output, lockfiles, formatting and
migrations. This is human guidance, not an absolute CI rejection threshold.
The initial governance baseline exceeds 500 lines because it introduces connected
policy, tooling, workflows and adversarial regression tests into an empty repo.

Fill the PR template truthfully. Small/documentation PRs may use brief sentences
and `N/A: reason` for inapplicable sections. Every evidence outcome needs an
explanation. Never infer a passing test from a checked box or prose. Attach commands,
results and relevant CI links; disclose failures and missing infrastructure.
See [testing](docs/engineering-governance/testing-policy.md),
[evidence](docs/engineering-governance/evidence-policy.md) and
[security review](docs/engineering-governance/security-review-policy.md).

Do not commit local secrets or credential files. Review dependency provenance,
license, maintenance, vulnerabilities and alternatives before adding one. Commit
the chosen package manager's lockfile and use its frozen install in CI when a
package stack is introduced; do not introduce multiple package managers casually.

Native rules and current activation gaps are documented in
[repository-rules.md](docs/engineering-governance/repository-rules.md). Policies apply
even where the current GitHub plan cannot enforce them. The owner must approve a
separate empty-repository bootstrap process; contributors must not seed `main` to
work around the PR requirement.
