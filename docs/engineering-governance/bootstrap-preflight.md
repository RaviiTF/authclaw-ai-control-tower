# Bootstrap preflight and execution record

Pre-authorization inspection: 2026-10-27 (Asia/Calcutta). The preflight sections
below preserve that historical snapshot; see the execution receipt at the end.

## Current state and scope

- Correct clone/origin: RaviiTF/authclaw-ai-control-tower in the authorized workspace.
- Local branch: `governance/engineering-baseline`, zero commits; existing reviewed
  governance files are saved and uncommitted with intent-to-add diff entries.
- GitHub CLI authentication succeeds as RaviiTF with admin access; no credentials
  were printed, requested, replaced or broadened.
- Remote visibility at this execution's start: **public**, already changed outside
  this agent's actions. Remote branches, workflows and runs: **zero**.
- Configured default: `main`, but that ref does not exist. Rulesets: HTTP 200 `[]`.
  Protection GET: HTTP 404, Branch not found. No effective merge protection claimed.
- Only RaviiTF is a collaborator. VidhiTF has public read permission, not qualifying
  write permission. No invitation or access change is authorized/performed yet.

## Security gate evidence

The complete governance diff, instructions, policies, workflows, template, parser,
tests and ignore rules were inspected. No real credentials, private keys, local
environment files, sensitive infrastructure configuration or confidential
operational material were identified in the reviewed publication candidates.
Account/repository names and governance status are intentionally disclosed here.
This is bounded static review plus scanning, not a guarantee of all secret types.

Gitleaks 8.30.1 directory scan with full redaction: exit 0, no findings.
Git's complete reachable history has **0 commits**; history scanning therefore
has no target history to validate. Separate safe positive/negative directory and
history fixtures prove detection and full redaction, including a deleted file's
committed synthetic token. No rules were weakened to pass the fixtures.

Ignored files were enumerated: only `scripts/__pycache__/` and `tests/__pycache__/`
bytecode appeared. These generated local artifacts are excluded from publication.
The .gitignore excludes local environment/credential files; the repository guard
also rejects force-added credential filenames. External workspace scanner binaries,
scratch fixtures and logs are outside the repository and will not be committed.

Fresh verification: 15 unit/CLI tests passed; repository hygiene passed; actionlint
1.7.12 passed; YAML/JSON configuration inspection passed; git diff whitespace check
passed. Hosted CI: **not run**. Linux workflow execution: **not verified**.

## Proposed auditable bootstrap (not authorized or performed)

1. Recheck remote refs and the final candidate diff immediately before publication.
   Stop if new remote/user work appeared; never overwrite or force-push.
2. With explicit authorization, create the first `main` commit containing exactly
   `README.md`, `scripts/governance.py` and `.github/CODEOWNERS`. This is a disclosed
   one-time initial-base exception, not a normal direct-push path. The parser is
   needed on the base so the initial governance PR cannot replace its own disclosure
   validator. CODEOWNERS is needed on the base for native review ownership.
3. Preserve the entire local tree; prepare the initial commit in a separate local
   temporary Git checkout rather than deleting or resetting these uncommitted files.
   Record its commit SHA, file list and results. Keep local scratch out of commits.
4. Publish the remaining reviewed governance baseline on
   `governance/engineering-baseline` and open an unmerged PR to `main`. In the
   separate checkout, create that feature branch **from the exact seed main
   commit**, then overlay the preserved governance candidates. Never commit the
   existing orphan branch independently: that would create unrelated histories.
   The initial base files remain unchanged in the PR. Provide actual results and
   explicit bootstrap disclosure in the PR body. No merge or self/automatic approval.
5. Separately obtain authorization to invite/grant VidhiTF write access. Wait for
   accepted qualifying access; public read permission is insufficient. The owner
   does not count as independent review. No eligible reviewer means no merge.
6. Inspect actual successful GitHub check contexts on the PR. Only then apply the
   reviewed protection payload to the verified branch, preserving stronger settings:
   one approval, CODEOWNERS, stale dismissal, latest-push approval, resolved
   conversations, successful observed checks, no force/deletion and admin enforcement.
   Do not create required contexts or owner requirements that have no usable run or
   reviewer. Read back protection and effective rules; verify on an unmerged PR.

This sequence needs explicit authorization for the initial base exception and
publication, and separate authorization for access changes. No remote write beyond
the prior authorized dependency-alert setting has been performed by this agent.

Independent preflight review found no security, CI or authorization defect. Its
ancestry clarification is incorporated in step 4; the reviewer independently ran
all 15 tests and repository hygiene successfully using workspace TEMP/TMP.

## Visibility restoration

Privacy remains the requested final state. Do not assume settings survive a move
to private: the earlier private-state protection APIs returned a plan restriction.
Secure a supported private-repository plan before relying on private enforcement.
Do not purchase a plan automatically. Existing public forks/copies, if created by
others, would not be made private by a later visibility change.

Before restoration, verify intended files remotely, actual successful CI, eligible
independent review and effective rules. Then obtain explicit authorization for the
private transition, change once, and read back visibility plus effective protection.
Report any plan/feature loss accurately. Never use repeated visibility changes as
a verification substitute. No visibility mutation has occurred in this execution.

## Execution receipt after explicit authorization

The owner approved both the exact three-file seed/publication PR and VidhiTF's
write-access invitation in this chat. Remote refs/rules/invitations were rechecked
before acting; no conflicting work or existing protection was present.

- Invitation 339959336 sent to VidhiTF with `write` permission; acceptance pending.
- Seed `df5237cb2dc66da7b14fb6b8c2e81893b62c12e1` created in a separate checkout
  using a repository-local GitHub noreply identity. Its tree contains exactly
  README.md, scripts/governance.py and .github/CODEOWNERS (136 lines).
- Seed directory and one-commit history scans passed without findings. Push was
  non-forced. Remote `main` readback matched the exact seed SHA and file tree.
- The feature branch was created from that seed and published as PR #1; unrelated
  orphan history was not published. The three approved seed files are unchanged.
- Hosted PR runs 40502040013 and 40502040015 passed all four checks at be68fa9.
  Active ruleset 25955410 now enforces no force/deletion and those app-bound
  required checks. Mandatory human/code-owner/latest-push approval is still pending
  accepted reviewer access. See publication-verification.md for exact limits.
- No merge, bypass, visibility change or unapproved access change occurred.
