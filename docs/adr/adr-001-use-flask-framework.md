# ADR 001: Use Flask Web Framework

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

We needed to select a Python web framework to build the vendor contract extraction web application. The primary requirements were:
- Simple and lightweight for an internal Maersk application
- Support for session-based authentication
- Quick development and deployment
- Suitable for Maersk's standard web application pattern

## Decision

We chose **Flask** over FastAPI, Django, or other Python web frameworks.

### Rationale

1. **Simplicity** - Flask's minimalist approach reduces complexity for a focused extraction tool
2. **Maersk Standard** - Flask aligns with Maersk's standard web application practices
3. **Quick Development** - Fewer abstractions than Django, less boilerplate than FastAPI
4. **Authentication Integration** - Flask-SQLAlchemy and Flask extensions support pluggable auth (LDAP, OAuth, SAML)
5. **Scalability** - Sufficient for internal use; can handle Maersk employee load
6. **Deployment** - Runs on standard Python, works with Docker (Maersk standard)

## Consequences

### Positive
- Fast iteration and development
- Easy to understand codebase for new team members
- Lightweight deployment (Docker image <500MB)
- Good debugging experience

### Negative
- Not suitable for ultra-high-traffic systems (but acceptable for internal use)
- Requires manual implementation of features Django provides out-of-box
- Limited built-in ORM structure (mitigated by Flask-SQLAlchemy)

## Alternatives Considered

1. **Django** - Too heavyweight for this use case
2. **FastAPI** - Overkill for a single-page web app; REST API focus not needed
3. **Bottle** - Too minimal; less ecosystem support

## Related Decisions

- [[adr-002-session-based-authentication.md]] - How authentication is handled
- [[adr-003-frontend-only-architecture.md]] - Web-only, no backend API
