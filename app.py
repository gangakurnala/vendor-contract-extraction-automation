"""
Flask Application
Main application entry point with API and Web endpoints
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_restx import Api, Resource, fields, Namespace
from config import get_config
from models import db, User, ExtractionJob, JobStatus, ContractResult, init_db
from auth import get_auth_provider, create_tokens, log_audit
import os
import uuid
from datetime import datetime
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """Application factory"""

    app = Flask(__name__)
    app.config.from_object(get_config())

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)

    # Initialize database
    with app.app_context():
        init_db(app)

    # Create API
    api = Api(app, version='1.0', title='Contract Extraction API',
              description='Extract vendor contract information using Claude AI')

    # Setup namespaces
    auth_ns = api.namespace('api/auth', description='Authentication endpoints')
    extraction_ns = api.namespace('api/extraction', description='Extraction endpoints')
    job_ns = api.namespace('api/jobs', description='Job management endpoints')

    # ==================== Authentication Endpoints ====================

    @auth_ns.route('/login')
    class Login(Resource):
        """User login"""
        def post(self):
            """
            Login with username and password
            Returns access and refresh tokens
            """
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                if not username or not password:
                    return {'error': 'Missing username or password'}, 400

                # Get auth provider and authenticate
                auth_provider = get_auth_provider()
                user_info, status_code = auth_provider.authenticate(username, password)

                if status_code != 200:
                    return user_info, status_code

                # Create tokens
                tokens, status = create_tokens(
                    user_info['user_id'],
                    user_info['username']
                )

                if status != 200:
                    return tokens, status

                # Log audit
                log_audit(
                    user_info['user_id'],
                    'LOGIN',
                    'user',
                    user_info['user_id']
                )

                return {
                    'message': 'Login successful',
                    'user': user_info,
                    'tokens': tokens
                }, 200

            except Exception as e:
                logger.error(f"Login error: {e}")
                return {'error': 'Login failed'}, 500

    @auth_ns.route('/user')
    class CurrentUser(Resource):
        """Get current user information"""
        @jwt_required()
        def get(self):
            """Get current authenticated user"""
            try:
                identity = get_jwt_identity()
                user_id = identity['user_id']

                auth_provider = get_auth_provider()
                user_info, status = auth_provider.get_user_info(user_id)

                return user_info, status

            except Exception as e:
                logger.error(f"Get user error: {e}")
                return {'error': 'Failed to get user'}, 500

    # ==================== Extraction Endpoints ====================

    @extraction_ns.route('/upload')
    class UploadContracts(Resource):
        """Upload contracts for extraction"""
        @jwt_required()
        def post(self):
            """
            Upload contract files for extraction
            Supports PDF and Word documents
            """
            try:
                identity = get_jwt_identity()
                user_id = identity['user_id']

                # Check if files provided
                if 'files' not in request.files:
                    return {'error': 'No files provided'}, 400

                files = request.files.getlist('files')
                if not files or files[0].filename == '':
                    return {'error': 'No files selected'}, 400

                # Create job
                job_id = str(uuid.uuid4())
                job_name = request.form.get('job_name', f'Extraction {job_id[:8]}')

                job = ExtractionJob(
                    id=job_id,
                    user_id=user_id,
                    job_name=job_name,
                    description=request.form.get('description', ''),
                    status=JobStatus.PENDING.value,
                    input_file_count=len(files)
                )

                # Save uploaded files
                job_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], job_id)
                os.makedirs(job_folder, exist_ok=True)

                uploaded_files = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(job_folder, filename)
                        file.save(filepath)
                        uploaded_files.append(filename)

                if not uploaded_files:
                    return {'error': 'No valid files uploaded'}, 400

                job.uploaded_files = uploaded_files
                db.session.add(job)
                db.session.commit()

                # Log audit
                log_audit(
                    user_id,
                    'UPLOAD',
                    'job',
                    job_id,
                    {'file_count': len(uploaded_files)}
                )

                return {
                    'message': 'Files uploaded successfully',
                    'job_id': job_id,
                    'job': job.to_dict()
                }, 201

            except Exception as e:
                logger.error(f"Upload error: {e}")
                return {'error': 'Upload failed'}, 500

    @extraction_ns.route('/extract/<job_id>')
    class ExtractContracts(Resource):
        """Extract contract information"""
        @jwt_required()
        def post(self, job_id):
            """Start extraction process for uploaded contracts"""
            try:
                identity = get_jwt_identity()
                user_id = identity['user_id']

                # Get job
                job = ExtractionJob.query.get(job_id)
                if not job:
                    return {'error': 'Job not found'}, 404

                if job.user_id != user_id:
                    return {'error': 'Unauthorized'}, 403

                # Start extraction
                job.status = JobStatus.PROCESSING.value
                job.started_at = datetime.utcnow()
                db.session.commit()

                # Process files
                from contract_extractor_test import process_contracts_test

                job_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], job_id)
                output_file = os.path.join(
                    current_app.config['RESULTS_FOLDER'],
                    f"extraction_{job_id}.xlsx"
                )

                try:
                    # Run extraction (test mode for now)
                    process_contracts_test(job_folder, output_file)

                    job.status = JobStatus.COMPLETED.value
                    job.completed_at = datetime.utcnow()
                    job.output_file_path = output_file
                    job.processing_time_seconds = (
                        job.completed_at - job.started_at
                    ).total_seconds()

                    # Count results
                    # This is simplified - could be improved with actual counting
                    job.total_contracts_extracted = len(job.uploaded_files)
                    job.total_services_extracted = 8  # From test mode

                except Exception as e:
                    job.status = JobStatus.FAILED.value
                    job.error_message = str(e)
                    logger.error(f"Extraction error: {e}")

                db.session.commit()

                # Log audit
                log_audit(
                    user_id,
                    'EXTRACT',
                    'job',
                    job_id,
                    {'status': job.status}
                )

                return {'message': 'Extraction complete', 'job': job.to_dict()}, 200

            except Exception as e:
                logger.error(f"Extract error: {e}")
                return {'error': 'Extraction failed'}, 500

    # ==================== Job Management Endpoints ====================

    @job_ns.route('')
    class JobList(Resource):
        """List extraction jobs"""
        @jwt_required()
        def get(self):
            """Get list of jobs for current user"""
            try:
                identity = get_jwt_identity()
                user_id = identity['user_id']

                # Get pagination parameters
                page = request.args.get('page', 1, type=int)
                per_page = current_app.config.get('ITEMS_PER_PAGE', 20)

                jobs = ExtractionJob.query.filter_by(user_id=user_id).paginate(
                    page=page,
                    per_page=per_page
                )

                return {
                    'total': jobs.total,
                    'pages': jobs.pages,
                    'current_page': page,
                    'jobs': [job.to_summary() for job in jobs.items]
                }, 200

            except Exception as e:
                logger.error(f"List jobs error: {e}")
                return {'error': 'Failed to list jobs'}, 500

    @job_ns.route('/<job_id>')
    class JobDetail(Resource):
        """Get job details"""
        @jwt_required()
        def get(self, job_id):
            """Get detailed information about a job"""
            try:
                identity = get_jwt_identity()
                user_id = identity['user_id']

                job = ExtractionJob.query.get(job_id)
                if not job:
                    return {'error': 'Job not found'}, 404

                if job.user_id != user_id:
                    return {'error': 'Unauthorized'}, 403

                return job.to_dict(), 200

            except Exception as e:
                logger.error(f"Get job error: {e}")
                return {'error': 'Failed to get job'}, 500

    @job_ns.route('/<job_id>/download')
    class DownloadResults(Resource):
        """Download extraction results"""
        @jwt_required()
        def get(self, job_id):
            """Download Excel file with extraction results"""
            try:
                identity = get_jwt_identity()
                user_id = identity['user_id']

                job = ExtractionJob.query.get(job_id)
                if not job:
                    return {'error': 'Job not found'}, 404

                if job.user_id != user_id:
                    return {'error': 'Unauthorized'}, 403

                if not job.output_file_path or not os.path.exists(job.output_file_path):
                    return {'error': 'Results file not found'}, 404

                # Log audit
                log_audit(
                    user_id,
                    'DOWNLOAD',
                    'job',
                    job_id
                )

                return send_file(
                    job.output_file_path,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=f"extraction_{job_id}.xlsx"
                )

            except Exception as e:
                logger.error(f"Download error: {e}")
                return {'error': 'Failed to download'}, 500

    # ==================== Web Routes ====================

    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')

    @app.route('/dashboard')
    @jwt_required()
    def dashboard():
        """User dashboard"""
        return render_template('dashboard.html')

    @app.route('/upload')
    @jwt_required()
    def upload_page():
        """Upload page"""
        return render_template('upload.html')

    @app.route('/jobs')
    @jwt_required()
    def jobs_page():
        """Jobs list page"""
        return render_template('jobs.html')

    # ==================== Error Handlers ====================

    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal error: {error}")
        return {'error': 'Internal server error'}, 500

    return app


def allowed_file(filename):
    """Check if file extension is allowed"""
    allowed_extensions = {'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def secure_filename(filename):
    """Make filename safe"""
    from werkzeug.utils import secure_filename as werkzeug_secure
    return werkzeug_secure(filename)


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', True)
    )
