"""
Application Configuration
Handles configuration for different environments (dev, production, test)
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False

    # Upload configuration
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), 'results')

    # Ensure upload folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///contract_extraction.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Authentication configuration
    AUTH_TYPE = os.getenv('AUTH_TYPE', 'test')  # 'test', 'ldap', 'oauth', 'saml'

    # LDAP Configuration (if AUTH_TYPE='ldap')
    LDAP_SERVER = os.getenv('LDAP_SERVER', 'ldap://localhost:389')
    LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=example,dc=com')
    LDAP_USER_DN = os.getenv('LDAP_USER_DN', 'ou=users,dc=example,dc=com')
    LDAP_ADMIN_DN = os.getenv('LDAP_ADMIN_DN', 'cn=admin,dc=example,dc=com')
    LDAP_ADMIN_PASSWORD = os.getenv('LDAP_ADMIN_PASSWORD', '')

    # OAuth Configuration (if AUTH_TYPE='oauth')
    OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID', '')
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET', '')
    OAUTH_AUTHORIZE_URL = os.getenv('OAUTH_AUTHORIZE_URL', '')
    OAUTH_ACCESS_TOKEN_URL = os.getenv('OAUTH_ACCESS_TOKEN_URL', '')
    OAUTH_USER_INFO_URL = os.getenv('OAUTH_USER_INFO_URL', '')

    # Celery configuration (for job queue)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # Anthropic API
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

    # Extraction settings
    EXTRACTION_MODEL = os.getenv('EXTRACTION_MODEL', 'claude-opus-5')
    EXTRACTION_MAX_TOKENS = int(os.getenv('EXTRACTION_MAX_TOKENS', 2048))

    # UI Settings
    ITEMS_PER_PAGE = 20
    MAX_UPLOAD_FILES = 10


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    # Use test mode for extraction (no API key needed)
    ANTHROPIC_API_KEY = ''


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    # Use test mode for extraction
    ANTHROPIC_API_KEY = ''


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Production uses real API key from environment
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
