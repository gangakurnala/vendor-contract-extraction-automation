# ADR 002: Use Session-Based Authentication (Not JWT)

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

Initially, the application used JWT tokens stored in browser localStorage and sent via Authorization headers. After initial development, the user requested removal of this JWT-based authentication in favor of simpler session-based authentication.

This decision reflects the evolution from a potential multi-service API architecture to a dedicated internal web application.

## Decision

We use **Flask session cookies** for authentication instead of JWT tokens.

### Implementation

- User logs in with username/password
- Flask creates an encrypted session cookie (httponly, secure)
- Session data (user_id) stored server-side
- Cookie automatically sent with each request
- No manual token management in JavaScript

## Consequences

### Positive
- **Simpler Frontend** - No localStorage token management needed
- **Better Security** - Cookies are httponly; no XSS vulnerability from token theft
- **Standard Pattern** - Familiar to web developers; no custom JWT handling
- **Automatic** - Browser automatically sends cookies with requests
- **Maersk Standard** - Aligns with Maersk's web authentication practices

### Negative
- **CSRF Consideration** - Must implement CSRF protection if form-based attacks are a concern
- **No Multi-Device** - Sessions tied to server; scaling requires session store (Redis/Memcached)
- **Not API-Friendly** - Can't be used for third-party API consumption
- **Server State** - Requires session storage; stateless scaling harder

## Alternatives Considered

1. **JWT Tokens** - Initial approach; removed per user request
2. **OAuth 2.0** - Overhead for internal-only app; can be added later
3. **API Keys** - Not suitable for interactive web application
4. **SAML** - Planned as optional auth provider but session-cookie transport remains

## Migration Notes

- Removed all localStorage token management from frontend
- Removed Authorization header from API calls
- Changed from `@jwt_required()` decorators to session checks in routes
- Simplified `apiCall()` JavaScript function (no token passing)

## Related Decisions

- [[adr-003-frontend-only-architecture.md]] - Web-only app; sessions sufficient
- [[adr-004-sqlalchemy-orm.md]] - Sessions stored in database
