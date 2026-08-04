# ADR 003: Frontend-Only Architecture (No Backend API)

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

Initial project design included both:
1. A REST API backend for other applications to consume extraction functionality
2. A web UI for Maersk employees to use interactively

After initial development and user testing, the user clarified: "remove the backend API functionality. this application will always be used by front end."

This decision reflects the actual business need: a dedicated internal web application for Maersk employees, not a shared microservice.

## Decision

The application is **frontend-only** with internal AJAX endpoints (not a REST API for external consumption).

### Architecture

- **Web Routes:** `/`, `/login`, `/logout`, `/dashboard`, `/upload`, `/jobs`
- **Internal AJAX Endpoints:** 
  - `/api/user` - Session check
  - `/api/extraction/upload` - File upload
  - `/api/extraction/extract` - Trigger extraction
  - `/api/jobs` - List jobs
  - `/api/jobs/<id>` - Job details
  - `/api/jobs/<id>/download` - Download results
- **No Public API:** Endpoints serve only the web frontend (localhost:5000)
- **Session-Based:** No API tokens; cookies handle auth

## Consequences

### Positive
- **Simpler Architecture** - No REST API versioning, documentation, or compatibility concerns
- **Better Security** - Internal-only endpoints; no external API attack surface
- **Faster Development** - Fewer abstractions; simpler request/response handling
- **Clear Purpose** - Single, focused application instead of multi-purpose API
- **Maersk Standard** - Aligns with internal web app pattern

### Negative
- **No Reusability** - Can't share extraction functionality with other systems
- **Scaling Limitations** - Horizontal scaling requires sticky sessions or session store
- **No API Documentation** - Endpoints are internal; minimal documentation needed
- **Frontend Coupling** - Backend tightly coupled to web UI

## Migration Path if Needed

If in future other systems need extraction capability:
1. Extract extraction logic to separate service
2. Create REST API frontend for that service
3. Current web app calls extraction service
4. Other systems call same extraction service

## Future Extensibility

- **Current:** Web-only app
- **Phase 2:** Could extract to extraction microservice if needed
- **Phase 3:** Then add REST API for external consumption

This maintains simplicity now while preserving architecture for future needs.

## Related Decisions

- [[adr-001-use-flask-framework.md]] - Flask chosen for web focus, not API
- [[adr-002-session-based-authentication.md]] - Session auth sufficient for single web app
- [[adr-006-excel-output-format.md]] - Web users download Excel files (not JSON APIs)
