# Security Policy

## Supported Versions

| Project | Supported Version |
| ------- | ----------------- |
| UMaT-Stuff Consolidated | 1.0.x |

## Reporting a Vulnerability

Security and privacy are paramount. If you discover a security vulnerability within any subproject of this repository, please report it responsibly:

1. **Do NOT open a public issue.**
2. Send an email or private report describing the vulnerability, proof-of-concept, and impact.
3. We will acknowledge receipt within 48 hours and work on a fix promptly.

## Security Practices
- Parameterized SQL queries for database interactions.
- Password hashing using `password_hash()` with `PASSWORD_DEFAULT`.
- Sanitization of HTML/XSS outputs.
