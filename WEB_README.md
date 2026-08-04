# Web Application - Contract Extraction Platform

Modern web application for contract extraction with REST API and Maersk authentication.

## Features

✅ **REST API** - For programmatic access and integration with other systems
✅ **Web Interface** - User-friendly dashboard for interactive use
✅ **Authentication** - Maersk LDAP, OAuth, SAML, or test mode
✅ **Job Management** - Track extraction jobs and results
✅ **Database Storage** - Persist results and audit logs
✅ **Docker Ready** - Production-ready containerized deployment

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         Maersk Users / Other Applications            │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    ┌───▼────────┐      ┌────▼──────────┐
    │   Web UI   │      │  REST API     │
    │ (Dashboard)│      │ (JSON/HTTP)   │
    └───┬────────┘      └────┬──────────┘
        │                    │
        └──────────┬─────────┘
                   │
        ┌──────────▼────────────┐
        │   Flask Application   │
        │  ├─ Authentication    │
        │  ├─ Job Management    │
        │  ├─ File Upload       │
        │  └─ Extraction Engine │
        └──────────┬────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    ┌───▼──┐  ┌───▼───┐  ┌──▼────┐
    │  DB  │  │Redis  │  │Files  │
    │(PG)  │  │(Cache)│  │(S3)   │
    └──────┘  └───────┘  └───────┘
```

## Installation

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/gangakurnala/vendor-contract-extraction-automation.git
cd vendor-contract-extraction-automation

# Create environment file
cp .env.web.example .env.web

# Edit with your configuration
nano .env.web

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web
```

Access at: http://localhost:5000

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements_web.txt

# Create environment file
cp .env.web.example .env.web

# Edit configuration
nano .env.web

# Initialize database
flask db upgrade

# Start development server
python app.py

# In another terminal, start Celery worker (optional)
celery -A tasks worker --loglevel=info
```

## Configuration

### Authentication Methods

#### 1. Test Mode (Development)
```bash
AUTH_TYPE=test
```
Accepts any username/password. Useful for development.

#### 2. Maersk LDAP
```bash
AUTH_TYPE=ldap
LDAP_SERVER=ldap://ldap.maersk.com:389
LDAP_BASE_DN=dc=maersk,dc=com
LDAP_USER_DN=ou=users
LDAP_ADMIN_DN=cn=admin,dc=maersk,dc=com
LDAP_ADMIN_PASSWORD=your_password
```

#### 3. OAuth (Maersk SSO)
```bash
AUTH_TYPE=oauth
OAUTH_CLIENT_ID=your_client_id
OAUTH_CLIENT_SECRET=your_client_secret
OAUTH_AUTHORIZE_URL=https://auth.maersk.com/authorize
OAUTH_ACCESS_TOKEN_URL=https://auth.maersk.com/token
OAUTH_USER_INFO_URL=https://auth.maersk.com/userinfo
```

#### 4. SAML
```bash
AUTH_TYPE=saml
# Additional SAML configuration needed
```

## API Endpoints

### Authentication
```
POST   /api/auth/login           - Login with credentials
GET    /api/auth/user            - Get current user (requires JWT)
```

### File Upload & Extraction
```
POST   /api/extraction/upload    - Upload contract files
POST   /api/extraction/extract/{job_id}  - Start extraction
```

### Job Management
```
GET    /api/jobs                 - List user's jobs
GET    /api/jobs/{job_id}        - Get job details
GET    /api/jobs/{job_id}/download - Download results Excel
```

## Usage Examples

### Login via API
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user@maersk.com", "password": "password"}'

# Response:
# {
#   "message": "Login successful",
#   "user": {"user_id": 1, "username": "user@maersk.com", ...},
#   "tokens": {"access_token": "...", "refresh_token": "..."}
# }
```

### Upload & Extract Files
```bash
# Upload files
curl -X POST http://localhost:5000/api/extraction/upload \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "files=@contract1.pdf" \
  -F "files=@contract2.docx" \
  -F "job_name=Q4 Contracts"

# Start extraction
curl -X POST http://localhost:5000/api/extraction/extract/{job_id} \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Get Results
```bash
# List jobs
curl http://localhost:5000/api/jobs \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Download Excel
curl http://localhost:5000/api/jobs/{job_id}/download \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o results.xlsx
```

## Web Interface

### Dashboard
- Overview of all extraction jobs
- Statistics: total, completed, processing, failed
- Quick access to recent jobs
- Upload new contracts

### Upload Page
- Drag-and-drop file upload
- Support for PDF and Word (.docx) files
- Job naming and description
- Progress tracking during extraction

### Jobs Page
- List all extraction jobs
- Search and filter
- View job details
- Download results

## Database

### Tables
- **users** - User accounts and authentication
- **extraction_jobs** - Extraction job records
- **contract_results** - Individual contract extraction results
- **audit_logs** - User action audit trail

### Supported Databases
- SQLite (development) - `sqlite:///contract_extraction.db`
- PostgreSQL (production) - `postgresql://user:password@host:5432/db`
- MySQL - Supported via SQLAlchemy

## Deployment to Maersk Infrastructure

### Kubernetes Deployment
```yaml
# Create ConfigMap
kubectl create configmap contract-extraction-config --from-file=.env.web

# Create Secret
kubectl create secret generic contract-extraction-secret \
  --from-literal=db-password=your-password

# Deploy
kubectl apply -f kubernetes/deployment.yaml
```

### Environment Variables for Production
```bash
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=long-random-secret-key
DATABASE_URL=postgresql://user:password@postgres-host:5432/contracts
ANTHROPIC_API_KEY=sk-ant-your-key
AUTH_TYPE=ldap
CELERY_BROKER_URL=redis://redis-host:6379/0
```

## Monitoring & Logging

### Docker Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f postgres
```

### Health Checks
```bash
# Web API
curl http://localhost:5000/api/health

# Database
docker-compose exec postgres pg_isready

# Redis
docker-compose exec redis redis-cli ping
```

## Performance Tuning

### For High Load
```bash
# Increase Gunicorn workers (docker-compose.yml)
gunicorn --workers 8 --worker-class sync

# Add Celery workers
docker-compose scale celery=4

# Database connection pooling
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_POOL_RECYCLE=3600
```

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check credentials
docker-compose logs postgres | grep -i error

# Restart database
docker-compose restart postgres
```

### Authentication Issues
```bash
# Check LDAP connection
ldapsearch -H ldap://ldap.maersk.com:389 -x

# Verify credentials
docker-compose logs web | grep -i ldap
```

### Jobs Not Processing
```bash
# Check Redis connection
docker-compose exec redis redis-cli ping

# Check Celery worker logs
docker-compose logs celery

# Restart worker
docker-compose restart celery
```

## Security Considerations

✅ **API Authentication** - JWT tokens for all API endpoints
✅ **Audit Logging** - All user actions logged
✅ **Database Security** - SQL injection protection via SQLAlchemy
✅ **File Upload** - Strict file type validation
✅ **HTTPS Ready** - Configure behind reverse proxy (nginx/haproxy)
✅ **Environment Secrets** - Use .env files (never commit)

### Production Checklist
- [ ] Change all default passwords and secrets
- [ ] Configure HTTPS/SSL certificate
- [ ] Set up reverse proxy (nginx)
- [ ] Enable database backups
- [ ] Configure logging to external system
- [ ] Set up monitoring and alerts
- [ ] Configure LDAP/OAuth with Maersk SSO
- [ ] Enable rate limiting on APIs
- [ ] Configure CORS for allowed domains

## Support & Documentation

- **API Docs**: http://localhost:5000/api/docs (Swagger UI)
- **Setup Guide**: See SETUP_GUIDE.md
- **Main README**: See README_DETAILED.md
- **Development Guide**: See CLAUDE.md

## License

Internal Maersk Project - Not for external distribution

---

**Version:** 2.0 (Web Application)
**Status:** Production Ready
**Last Updated:** August 2026
