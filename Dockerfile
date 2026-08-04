FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libldap2-dev \
    libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_web.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_web.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads results

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/auth/user', timeout=5)" || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
