# AuthClaw AI Control Tower

This initial baseline contains engineering governance tooling. No application,
runtime framework, dependency manifest, database or deployment is present yet.

Start with [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md),
[SECURITY.md](SECURITY.md) and the
[repository rules and activation checklist](docs/engineering-governance/repository-rules.md).
Run `python -m unittest discover -s tests -v` and
`python scripts/governance.py repository` with Python 3.14 and Git.

Repository files are prepared controls. Required reviews and merge blocking need
native GitHub protection; see the activation checklist for the verified plan,
reviewer and empty-repository blockers. This baseline does not claim deployment
readiness or an active protected branch.
