# Security policy

There is no released application or supported runtime version yet.
Do not put credentials, exploit details involving live systems, or sensitive tenant
data in public issues, PR descriptions or workflow logs.

For a vulnerability, use this repository's **Security > Report a vulnerability**
only if GitHub shows that feature enabled. Its availability has not been verified.
Otherwise arrange a private channel with the repository owner, RaviiTF, using an
existing trusted contact method before sending details. No reporting email or
response SLA is established. If no private route is available, request a private
route without disclosing vulnerability details publicly.

Include affected revision/components, impact, safe reproduction, evidence with
secrets redacted and any remediation suggestions. Do not test production systems
or access other tenants without authorization. Do not rotate/revoke credentials
without owner authorization. A discovered committed secret needs containment,
owner-authorized rotation and a separately authorized history-remediation plan;
deleting the current file alone does not remove prior exposure.

Security-sensitive changes follow
[security-review-policy.md](docs/engineering-governance/security-review-policy.md).
Native protection, CODEOWNERS and dependency/security features have separate
activation requirements; see
[repository-rules.md](docs/engineering-governance/repository-rules.md).
