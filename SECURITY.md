# Security Policy

## Reporting Vulnerabilities

Report security vulnerabilities to **security@telebotstudio.com**.

Do **not** file public issues for security vulnerabilities.

## What Counts as a Security Vulnerability

- Authentication bypass or credential exposure
- Path traversal or injection vulnerabilities
- Denial-of-service via malformed inputs
- Unauthorized access to session credentials
- Any flaw that compromises data confidentiality or integrity

The following are **not** security vulnerabilities:

- Bugs in functionality (use GitHub Issues)
- Feature requests or documentation errors
- Rate limiting or quota exhaustion

## Response Timeline

| Stage | Target |
|---|---|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 5 business days |
| Status updates | Every 5 business days until resolved |

## Supported Versions

Only the **latest stable release** receives security fixes.

## Credential Handling

This server handles API keys and bot tokens exclusively **in memory**. Credentials are:

- Never written to disk or logs
- Isolated per session
- Masked in all responses and previews

If you believe credentials may have been exposed, rotate them immediately and report the incident.
