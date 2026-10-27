# Security review policy

Explicit risk disclosure, relevant verification evidence and appropriate human
security-owner review are required for changes to authentication/session handling,
authorization/permissions, tenant isolation, runtime policy enforcement, gateway
trust boundaries, audit logs/evidence integrity, secrets, database access controls,
IAM/infrastructure permissions, deployment workflows, security tests or quality gates.

Describe affected boundaries and abuse/failure cases in Security impact, tests and
remaining uncertainty in Evidence, and recovery in Rollback. Inspect realistic
denied/allowed paths and affected middleware, policies and collaborators; do not
weaken them to make tests pass. A security owner must assess risks and tests.
Evidence-integrity changes include the governance validators and workflows here.

The owner selected **@VidhiTF** for independent security review. CODEOWNERS covers
every path, including future code, with that account. **@RaviiTF** remains the
repository administrator but does not count as the independent reviewer. One
qualifying non-author code-owner approval is required; two approvals are not
required. If VidhiTF authors a PR, another explicitly authorized independent
reviewer must be designated and made eligible before it can merge.

VidhiTF currently has public read access, not qualifying write access. The owner
explicitly authorized a write-access invitation; it was sent and is pending
acceptance. Verify accepted write access before relying on that entry.
CODEOWNERS has no mandatory
effect until it exists on the PR base and native **Require review from Code
Owners** is enabled. Native rules must also require at least one approval,
dismiss stale approvals and require approval of the latest reviewable push by
someone other than its pusher. A bot run is not a human review. Do not auto-approve
or self-approve. If no eligible non-author owner exists, leave the PR unmerged.

As the application grows, refine ownership only with real approved identities and
verified path coverage. Never exempt governance files or security tests casually.
