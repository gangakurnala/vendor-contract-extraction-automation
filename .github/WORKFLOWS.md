# GitHub Actions CI/CD Workflows

This project includes automated workflows for continuous integration, testing, code quality checks, deployment, and releases.

## 📋 Available Workflows

### 1. **CI - Test & Build** (`.github/workflows/ci.yml`)
**Triggers:** On every push to `main` or `develop`, and on pull requests

**What it does:**
- ✅ Runs tests on Python 3.8, 3.9, 3.10, 3.11
- ✅ Code linting with `flake8`
- ✅ Code formatting checks with `black`
- ✅ Import sorting with `isort`
- ✅ Unit tests with `pytest` and coverage reporting
- ✅ Uploads coverage to Codecov
- ✅ Builds Docker image

**Jobs:**
- `test` - Runs all tests and linting
- `build` - Builds Docker image
- `code-quality` - Additional security and quality checks

**View results:** Go to Actions tab → CI - Test & Build

---

### 2. **Deploy to Production** (`.github/workflows/deploy.yml`)
**Triggers:** Manually or when CI workflow succeeds on `main` branch

**What it does:**
- ✅ Builds Docker image
- ✅ Tags with commit SHA
- ✅ Ready for deployment

**Manual trigger:**
```bash
# Go to GitHub Actions → Deploy to Production → Run workflow
```

**TODO: Add deployment steps**
- Push Docker image to registry (Docker Hub, ECR, etc.)
- Deploy to Kubernetes, Cloud Run, App Engine, etc.
- SSH and pull latest image

---

### 3. **Release** (`.github/workflows/release.yml`)
**Triggers:** When you push a tag matching `v*` (e.g., `v1.0.0`)

**What it does:**
- ✅ Creates GitHub release with changelog
- ✅ Builds versioned Docker image
- ✅ Generates release notes

**How to use:**
```bash
# Create a tag and push
git tag v1.0.0
git push origin v1.0.0

# Or use GitHub UI:
# Releases → Draft a new release → Create release
```

**Result:** Automatic release with Docker image ready to deploy

---

## 🚀 Quick Start

### 1. **View Workflow Status**
- Go to your GitHub repository
- Click **Actions** tab
- See all workflow runs

### 2. **Fix Failing Tests**
If CI fails:
1. Click the failed workflow
2. Click the failed job
3. Scroll to find error details
4. Fix the issue locally
5. Push to trigger workflow again

### 3. **Create a Release**
```bash
# Tag the current commit
git tag v1.0.0

# Push the tag (triggers Release workflow)
git push origin v1.0.0

# View the release on GitHub
# Releases tab shows auto-generated release notes
```

### 4. **Manual Deployment**
- Go to **Actions** tab
- Select **Deploy to Production**
- Click **Run workflow**
- Select the branch (main)
- Click **Run workflow** button

---

## 📊 Test Reports

### View Coverage
After each CI run:
1. Click the `test` job
2. Scroll to **Upload coverage to Codecov**
3. Click the Codecov link to see detailed coverage report

### Download Artifacts
CI workflow generates:
- HTML coverage report
- Test results

---

## 🔧 Configuration

### Environment Variables & Secrets
Add secrets in GitHub:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets:

**Example secrets:**
```
ANTHROPIC_API_KEY          # API key for production
DOCKERHUB_USERNAME         # Docker Hub username
DOCKERHUB_TOKEN            # Docker Hub password
SLACK_WEBHOOK_URL          # Slack notifications
DEPLOYMENT_SERVER          # Production server IP/domain
DEPLOYMENT_USER            # SSH username
DEPLOYMENT_KEY             # SSH private key
```

### Using Secrets in Workflows
```yaml
env:
  API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# Or pass to docker run:
docker run -e ANTHROPIC_API_KEY=${{ secrets.ANTHROPIC_API_KEY }} ...
```

---

## 📝 Adding Custom Steps

### Example: Deploy to AWS
```yaml
- name: Deploy to AWS
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: |
    aws s3 cp . s3://my-bucket/ --recursive
```

### Example: Send Slack Notification
```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1.24.0
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Build ${{ job.status }} for ${{ github.ref }}"
      }
```

---

## 🐛 Troubleshooting

### Tests fail locally but pass in CI
- Check Python version: `python --version`
- Install all dependencies: `pip install -r requirements.txt -r requirements_web.txt`
- Clear cache: `rm -rf .pytest_cache`

### Coverage report is too low
- Add tests for uncovered lines
- Run locally: `pytest --cov`
- View report: `open htmlcov/index.html`

### Docker build fails
- Check Dockerfile syntax
- Build locally: `docker build .`
- Check file permissions

### Workflow not triggered
- Check branch name (must be `main` or `develop`)
- Check tag format (must be `v*` for releases)
- Check file paths in `on:` section

---

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [PyTest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)

---

## ✅ Checklist for Production

Before deploying to production:
- [ ] All tests pass
- [ ] Code coverage > 80%
- [ ] No security vulnerabilities (bandit)
- [ ] All linting passes (flake8)
- [ ] Docker image builds successfully
- [ ] Changelog updated
- [ ] Version tag created
- [ ] Release created on GitHub
- [ ] Deployment configured in `deploy.yml`
- [ ] Environment variables set in Secrets

---

**Last Updated:** August 2026
**Status:** Ready for customization
