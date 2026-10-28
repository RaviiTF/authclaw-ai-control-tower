# Evidence policy

For PRs and final agent reports distinguish:

| Outcome | Required disclosure |
| --- | --- |
| Passed | Executed command, result, revision/context and output or CI link |
| Failed | Executed command, failure, root cause/disposition and retest if fixed |
| Not run | Specific omitted check and reason |
| Blocked | Missing dependency, permission, service, secret or infrastructure |
| Static inspection | Scope reviewed and runtime behavior still unproven |
| Integration/E2E | Actual interfaces, collaborators and behavior exercised |

Use `None: explanation` or `N/A: explanation` where appropriate. Record fresh
evidence after the final change. Mocks, static review and green CI alone do not
prove middleware, authorization, tenant isolation, database policies, migrations,
workers, concurrency or deployed behavior. Choose real boundary checks when those
are affected; identify anything that remains unverified.

`PR disclosure` checks required headings, explained fields and six outcome labels
using the base revision's parser. It rejects empty/template/hidden-only sections.
It treats PR text as data and prints field names, not body contents. It cannot
verify truth, test adequacy, reviewer judgment, or whether arbitrary prose matches
the change. Even a fabricated explanation can pass structural validation; human
review and actual CI output remain necessary. The workflow itself is reviewed
code and needs native code-owner protection against weakening.

Never claim branch protection or a disabled Merge button from files alone. Verify
remote settings separately and distinguish configured, executed and blocked states.
Never publish secret values in evidence; scanner output must be fully redacted.

The prospective `Governance Gate` additionally checks live GitHub review records,
current collaborator permission and exact-head approval under a base-pinned policy,
plus Git-derived growth limits. PR-body approval markers have no authority. It
still does not authenticate arbitrary test/security prose or replace native merge
rules. See automated-gate.md for freshness, installation and verification limits.
