# Security Policy

## Supported versions

`fleet-mode` is actively maintained. Security fixes target the latest version on
the `main` branch.

| Version          | Supported |
| ---------------- | --------- |
| latest (`main`)  | ✅        |
| older tags       | ❌        |

## Reporting a vulnerability

Please **do not** open a public issue for security vulnerabilities.

Report privately through GitHub's
[**Report a vulnerability**](https://github.com/Jott2121/fleet-mode/security/advisories/new)
flow (the repository's **Security → Advisories** tab). I aim to acknowledge
reports within 72 hours and to ship a fix or mitigation for confirmed issues as
quickly as is practical.

When reporting, please include:

- a description of the issue and its impact,
- steps to reproduce (a minimal proof-of-concept if possible), and
- any suggested remediation.

## Scope

`fleet-mode` ships a Claude Code skill plus helper scripts (notably the
hash-chained receipt writer). Findings of particular interest: tampering with
the append-only receipt ledger, unsafe file handling in the scripts, and
supply-chain risks in CI (this repository pins its GitHub Actions to commit SHAs
and runs CodeQL + Dependabot to reduce that surface).

Thanks for helping keep it solid.
