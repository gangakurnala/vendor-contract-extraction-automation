"""
Database Models
Defines data structures for storing extraction jobs, results, and user data
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and tracking"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    extraction_jobs = db.relationship('ExtractionJob', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'department': self.department,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class JobStatus(str, Enum):
    """Extraction job status"""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class ExtractionJob(db.Model):
    """Extraction job model for tracking contract processing"""
    __tablename__ = 'extraction_jobs'

    id = db.Column(db.String(36), primary_key=True)  # UUID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default=JobStatus.PENDING.value)

    # File information
    input_file_count = db.Column(db.Integer, default=0)
    uploaded_files = db.Column(db.JSON, default=list)  # List of uploaded filenames

    # Results
    output_file_path = db.Column(db.String(255), nullable=True)
    total_contracts_extracted = db.Column(db.Integer, default=0)
    total_services_extracted = db.Column(db.Integer, default=0)
    extraction_results = db.Column(db.JSON, nullable=True)  # Store raw results

    # Error handling
    error_message = db.Column(db.Text, nullable=True)
    error_details = db.Column(db.JSON, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Processing info
    processing_time_seconds = db.Column(db.Float, nullable=True)
    celery_task_id = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_name': self.job_name,
            'description': self.description,
            'status': self.status,
            'input_file_count': self.input_file_count,
            'uploaded_files': self.uploaded_files,
            'output_file_path': self.output_file_path,
            'total_contracts_extracted': self.total_contracts_extracted,
            'total_services_extracted': self.total_services_extracted,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'processing_time_seconds': self.processing_time_seconds,
            'updated_at': self.updated_at.isoformat()
        }

    def to_summary(self):
        """Return summary for list view"""
        return {
            'id': self.id,
            'job_name': self.job_name,
            'status': self.status,
            'input_file_count': self.input_file_count,
            'total_contracts_extracted': self.total_contracts_extracted,
            'total_services_extracted': self.total_services_extracted,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


class ContractResult(db.Model):
    """Individual contract extraction result"""
    __tablename__ = 'contract_results'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey('extraction_jobs.id'), nullable=False)

    # Contract information
    contract_number = db.Column(db.String(100), nullable=True)
    vendor_name = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.String(50), nullable=True)
    end_date = db.Column(db.String(50), nullable=True)
    contract_value = db.Column(db.String(100), nullable=True)
    payment_terms = db.Column(db.String(100), nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    contract_type = db.Column(db.String(100), nullable=True)

    # Services (JSON array)
    services = db.Column(db.JSON, default=list)

    # Source information
    source_filename = db.Column(db.String(255), nullable=True)
    extraction_score = db.Column(db.Float, nullable=True)  # Confidence score

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'contract_number': self.contract_number,
            'vendor_name': self.vendor_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'contract_value': self.contract_value,
            'payment_terms': self.payment_terms,
            'currency': self.currency,
            'contract_type': self.contract_type,
            'services': self.services,
            'source_filename': self.source_filename,
            'extraction_score': self.extraction_score,
            'created_at': self.created_at.isoformat()
        }


class AuditLog(db.Model):
    """Audit log for tracking user actions"""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(100), nullable=False)  # e.g., 'job', 'contract'
    resource_id = db.Column(db.String(255), nullable=True)
    details = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat()
        }


def init_db(app):
    """Initialize database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
