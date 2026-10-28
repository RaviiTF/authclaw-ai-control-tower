# Engineering instructions

This repository currently contains governance tooling only. Do not infer an
application framework, database, deployment target, or passing runtime tests.
Read CONTRIBUTING.md and the relevant docs/engineering-governance policies.
Nested instructions, if introduced for a concrete need, refine these rules.

1. Before editing, confirm repository, branch, status, relevant diffs, architecture,
   entry points, dependencies, documentation and existing conventions. Trace the
   affected behavior end to end. Preserve unrelated and uncommitted user changes.
2. Make the smallest readable, maintainable change that meets the request. Reuse
   existing utilities. Avoid unrelated edits, speculative abstractions, duplicated
   implementations, dead code and new dependencies without justification.
3. Preserve behavior and security boundaries unless explicitly asked to change
   them. Never weaken authentication, authorization, tenant isolation, runtime
   enforcement, audit evidence, database policies or quality gates to pass tests.
4. Never hardcode, commit or print secrets. Keep local credentials out of Git.
   Use sanitized examples. If a secret is found, report the path without its value;
   recommend remediation without rotating or revoking credentials unasked.
5. Add meaningful regression tests through realistic public interfaces when
   behavior changes. Run relevant checks; diagnose, fix and retest failures.
   For current tooling: `python -m unittest discover -s tests -v` and
   `python scripts/governance.py repository`. Run actionlint and Gitleaks as
   described in testing-policy.md. New stacks must add real lint/type/test/build,
   dependency/lockfile, integration and migration checks as applicable.
6. Review error handling, security, concurrency, compatibility, data integrity,
   maintainability and performance. Compare with the original and simplify safely;
   never remove meaningful tests or protections just to reduce LOC. Retest changes.
   Use a bounded independent reviewer when available; disclose if unavailable.
7. Follow evidence-policy.md: separate passed, failed, not-run, blocked, static and
   integration/E2E evidence. Never claim a file, test, feature, deployment or remote
   setting changed or passed without fresh evidence. Identify unverified
   assumptions, known limitations, significant dependencies and architecture changes.
8. Every change goes through a feature branch and PR. Never push directly to the
   default branch, self-approve, auto-approve for a human, bypass required reviews,
   CI or permissions, or merge without explicit owner authorization. A bot's CI
   success is not a qualifying human approval. No eligible reviewer means no merge.
   The repository owner does not count as the independent reviewer. Do not invite
   collaborators or change permissions without explicit authorization.
9. Destructive operations, history rewrites, unrelated external writes, production
   changes, secret rotation and changes to recovery access need explicit authority.
   A default-branch bootstrap needs separate explicit, auditable authorization;
   the initial three-file seed has that authorization. It does not authorize a merge.
   Visibility changes require explicit authorization and a secret/confidentiality
   preflight. Read back effective rules after any authorized visibility change;
   never assume public-only protections survive restoration of private visibility.
10. Report fixes/files, any safe complexity reduction, actual checks/results,
    independent review and remaining limitations concisely. Complete review, fix,
    tests, independent review and fresh integrated verification before claiming done.
