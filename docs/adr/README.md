# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the Vendor Contract Extraction Application.

An ADR documents an important architectural decision, the context leading to it, and the consequences of that choice.

## ADRs Overview

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](adr-001-use-flask-framework.md) | Use Flask Web Framework | Accepted | 2026-08-04 |
| [ADR-002](adr-002-session-based-authentication.md) | Session-Based Authentication (Not JWT) | Accepted | 2026-08-04 |
| [ADR-003](adr-003-frontend-only-architecture.md) | Frontend-Only Architecture (No Backend API) | Accepted | 2026-08-04 |
| [ADR-004](adr-004-sqlalchemy-orm.md) | SQLAlchemy ORM with SQLite (Dev) / PostgreSQL (Prod) | Accepted | 2026-08-04 |
| [ADR-005](adr-005-claude-sonnet-integration.md) | Claude Sonnet 5.0 for Contract Extraction | Accepted | 2026-08-04 |
| [ADR-006](adr-006-excel-output-format.md) | Excel Output Format for Extracted Data | Accepted | 2026-08-04 |
| [ADR-007](adr-007-asynchronous-processing.md) | Asynchronous Job Processing (Celery + Redis) | Accepted | 2026-08-04 |

## Quick Reference

### Technology Stack
- **Web Framework:** Flask (ADR-001)
- **Authentication:** Session Cookies (ADR-002)
- **Database:** SQLAlchemy ORM + SQLite/PostgreSQL (ADR-004)
- **AI Extraction:** Claude Sonnet 5.0 (ADR-005)
- **Output:** Excel Workbooks (ADR-006)
- **Processing:** Synchronous (dev) / Async with Celery (prod) (ADR-007)

### Architecture Style
- **Single-Purpose:** Internal web application for Maersk employees (ADR-003)
- **No External APIs:** Frontend-only architecture
- **Session-Based Security:** User authentication via session cookies

### Data Flow
```
User Upload
    ↓
Web Form (Flask route)
    ↓
Extract Contracts (Claude API)
    ↓
Store in Database (SQLAlchemy)
    ↓
Generate Excel File (openpyxl)
    ↓
User Download (.xlsx)
```

## Reading ADRs

Each ADR has these sections:
- **Status** - Proposed, Accepted, Deprecated, Superseded
- **Context** - What problem are we solving?
- **Decision** - What did we decide?
- **Consequences** - What are the tradeoffs?
- **Alternatives Considered** - Why not other options?
- **Related Decisions** - Links to other ADRs

## Decision Dependencies

```
ADR-001 (Flask)
    ↓
    ├→ ADR-002 (Session Auth)
    ├→ ADR-003 (Frontend-Only)
    └→ ADR-004 (SQLAlchemy)
        ↓
        ├→ ADR-005 (Claude)
        ├→ ADR-006 (Excel Output)
        └→ ADR-007 (Async Processing)
```

## Creating New ADRs

When considering a significant architectural change:

1. Create file: `adr-NNN-decision-title.md`
2. Use template (see any ADR above)
3. Fill out all sections
4. Get stakeholder review
5. Update this README with link
6. Mark as "Accepted" when approved

### Superseding an ADR

If a decision is reversed:
1. Change old ADR status to "Superseded by ADR-XXX"
2. Create new ADR with status "Accepted"
3. Update README

## Querying ADRs

**By Concern:**
- Authentication: ADR-002
- Data Storage: ADR-004
- Processing Pipeline: ADR-005, ADR-006, ADR-007
- User Interface: ADR-003
- Technology Selection: ADR-001

**By Status:**
- Accepted: All current ADRs (001-007)
- Proposed: None
- Deprecated: None
- Superseded: None

**By Date:**
- 2026-08-04: All current ADRs

## Related Documentation

- [CLAUDE.md](../../CLAUDE.md) - Development guidelines and project overview
- [README_DETAILED.md](../../README_DETAILED.md) - Feature documentation
- [SETUP_GUIDE.md](../../SETUP_GUIDE.md) - Installation and deployment

---

**Last Updated:** 2026-08-04
**Total ADRs:** 7
**Acceptance Rate:** 100%
