"""
WSGI entry point for production deployment
"""

import os
from app import create_app, db
from models import User, ExtractionJob, ContractResult, AuditLog

app = create_app(os.getenv('FLASK_ENV', 'production'))

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
