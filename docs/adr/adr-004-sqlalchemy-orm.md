# ADR 004: Use SQLAlchemy ORM with SQLite (Dev) / PostgreSQL (Prod)

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

The application needs to store:
- User accounts and sessions
- Extraction jobs and their status
- Contract extraction results
- Audit logs for compliance

We needed to select a database and ORM strategy that supports:
- Development simplicity (no database setup needed)
- Production robustness (PostgreSQL standard)
- Easy migrations (evolving schema)
- Data integrity and audit trails

## Decision

Use **SQLAlchemy ORM** with:
- **Development:** SQLite (single file database)
- **Production:** PostgreSQL (enterprise-grade)

### Implementation

- `models.py` defines: User, ExtractionJob, ContractResult, AuditLog models
- Flask-SQLAlchemy integration handles session management
- DATABASE_URL in config supports both SQLite and PostgreSQL connection strings
- Pydantic models validate extracted data before storage

## Consequences

### Positive
- **Zero Setup for Dev** - SQLite requires no configuration; works immediately
- **Production Grade** - PostgreSQL supports scaling, replication, backups
- **Migrations** - Can use Alembic for schema versioning (future)
- **Type Safety** - Pydantic + SQLAlchemy provides strong data validation
- **Audit Ready** - AuditLog model supports compliance requirements
- **Maersk Standard** - PostgreSQL aligns with enterprise standards

### Negative
- **Dual Database Support** - SQLite/PostgreSQL differences may require testing
- **Migration Complexity** - Moving from SQLite to PostgreSQL requires export/import
- **No ORM Migrations Tool** - Currently manual; Alembic would improve this
- **Complexity** - More than simple file storage; overkill for very small apps

## Data Models

```
User
├── id (PK)
├── username (unique)
├── password_hash
├── auth_provider (test, ldap, oauth, saml)
└── created_at

ExtractionJob
├── id (PK)
├── user_id (FK to User)
├── job_name
├── status (pending, processing, completed, failed)
├── input_file_count
├── uploaded_files (JSON)
├── total_contracts_extracted
├── total_services_extracted
├── output_file_path
├── processing_time_seconds
├── error_message
└── created_at, completed_at

ContractResult
├── id (PK)
├── job_id (FK to ExtractionJob)
├── contract_number
├── vendor_name
├── contract_value
├── dates, terms, etc.

AuditLog
├── id (PK)
├── user_id (FK to User)
├── action (login, upload, extraction, download)
├── resource (job_id, contract_id)
└── timestamp
```

## Alternatives Considered

1. **Raw SQL** - More control; less type safety; error-prone
2. **Mongo/NoSQL** - Good for flexible schemas; overkill for structured contracts
3. **File-Based Storage** - Simpler; no audit trail; poor for scaling
4. **ORM Alternatives (Tortoise, Peewee)** - Less mature; smaller community

## Deployment Strategy

**Development:**
```python
DATABASE_URL=sqlite:///contract_extraction.db
```

**Production:**
```python
DATABASE_URL=postgresql://user:password@host:5432/contracts
```

## Future Enhancements

- [ ] Add Alembic for schema migrations
- [ ] Add database connection pooling for production
- [ ] Implement read replicas for PostgreSQL
- [ ] Add data archival for completed jobs

## Related Decisions

- [[adr-002-session-based-authentication.md]] - Sessions stored in database
- [[adr-007-asynchronous-processing.md]] - Job status tracking in database
