# ADR 007: Asynchronous Job Processing (Celery + Redis for Production)

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

Contract extraction is **long-running**:
- Each contract takes 30-60 seconds (Claude API latency)
- A batch of 10 contracts = 5-10 minutes
- User should not wait for extraction; they expect a job to complete in background

Requirements:
- User uploads contracts → gets job ID → can check status anytime
- Extraction happens asynchronously (not blocking web request)
- Job status visible in dashboard (pending, processing, completed, failed)
- Users can download results once completed

## Decision

Implement **asynchronous job processing** using:
- **Development:** Single-threaded Flask (jobs processed sequentially, synchronously)
- **Production:** Celery + Redis (distributed task queue, parallel processing)

### Implementation

```python
# Current (Development)
@app.route('/api/extraction/extract/<job_id>', methods=['POST'])
def extract(job_id):
    # Synchronous: blocks until complete
    job = ExtractionJob.query.get(job_id)
    job.status = 'processing'
    result = extract_contracts(job)
    job.status = 'completed'
    return {'status': 'completed'}

# Production (with Celery)
@celery.task
def extract_contracts_async(job_id):
    # Async: returns immediately; Celery worker executes in background
    job = ExtractionJob.query.get(job_id)
    job.status = 'processing'
    result = extract_contracts(job)
    job.status = 'completed'

@app.route('/api/extraction/extract/<job_id>', methods=['POST'])
def extract(job_id):
    # Trigger async task; return immediately
    extract_contracts_async.delay(job_id)
    return {'status': 'processing', 'job_id': job_id}
```

### Development Flow (Synchronous)

1. User uploads contracts → ExtractionJob created with status=pending
2. User clicks "Extract" → Flask processes synchronously
3. User waits (page shows loading spinner)
4. When done, results available for download

**Note:** Development is synchronous for simplicity; no Celery/Redis needed.

### Production Flow (Asynchronous)

1. User uploads contracts → ExtractionJob created with status=pending
2. User clicks "Extract" → Celery task queued; API returns immediately
3. Celery worker picks up task from Redis
4. User can check dashboard to see status
5. When complete, user downloads results

## Consequences

### Positive
- **Non-Blocking** - Web requests return instantly; UX not degraded by long-running tasks
- **Scalable** - Multiple Celery workers process jobs in parallel
- **Resilient** - Failed jobs retry automatically; won't lose extraction results
- **Trackable** - Job status visible in database and dashboard
- **Production-Ready** - Supports high-volume extraction scenarios

### Negative
- **Operational Complexity** - Production requires Redis, Celery, workers
- **Debugging Harder** - Async errors happen in worker process, not web request
- **Dual Code Paths** - Dev has sync code; production has async (must maintain both)
- **Dev/Prod Parity** - May behave differently during development vs production
- **Redis Dependency** - Production scaling requires Redis uptime

## Job Status Lifecycle

```
pending ──→ processing ──→ completed ──✓ (download available)
                │
                └──→ failed ──✓ (error message shown)
```

## Configuration

**Development (.env.web):**
```
CELERY_ENABLED=false  # Synchronous processing
```

**Production (.env):**
```
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
CELERY_ENABLED=true
```

## Database Schema

```
ExtractionJob
├── id (UUID)
├── user_id
├── job_name
├── status (pending | processing | completed | failed)
├── uploaded_files (JSON array)
├── total_contracts_extracted
├── total_services_extracted
├── output_file_path
├── processing_time_seconds
├── error_message (if failed)
├── created_at
├── completed_at
└── updated_at (for polling)
```

## Frontend Integration

```javascript
// User uploads and clicks "Extract"
POST /api/extraction/extract/job-123
Response: { status: 'processing', job_id: 'job-123' }

// Poll for status every 2 seconds
GET /api/jobs/job-123
Response: { status: 'processing', contracts_extracted: 0, ... }

// When status = 'completed'
GET /api/jobs/job-123/download
→ Download .xlsx file
```

## Scaling Considerations

**Single Server (Development):**
- 1 Flask app, 1 SQLite database
- Synchronous extraction (one job at a time)
- Fine for <10 jobs/day

**Small Production (10-100 jobs/day):**
- 1 Flask app, PostgreSQL
- 1 Celery worker, Redis (single instance)
- Can process ~4-5 jobs concurrently

**Large Production (1000+ jobs/day):**
- N Flask apps (load balanced)
- PostgreSQL with replication
- N Celery workers across cluster
- Redis cluster for job queue

## Related Decisions

- [[adr-004-sqlalchemy-orm.md]] - Job status stored in PostgreSQL
- [[adr-003-frontend-only-architecture.md]] - Web UI polls job status via /api/jobs/<id>

## Future Enhancements

- [ ] Implement Celery Beat for scheduled extractions
- [ ] Add priority queues (VIP contractors processed first)
- [ ] Implement job rate limiting (max 100 concurrent)
- [ ] Add email notifications when job completes
- [ ] Implement job cost tracking (API tokens spent)
