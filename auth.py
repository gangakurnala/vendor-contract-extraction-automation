"""
Authentication Module
Supports multiple authentication methods: Test, LDAP, OAuth, SAML
"""

from flask import current_app, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from models import db, User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AuthProvider:
    """Base authentication provider"""

    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        raise NotImplementedError

    def get_user_info(self, user_id):
        """Get user information"""
        raise NotImplementedError


class TestAuthProvider(AuthProvider):
    """Test authentication provider (no actual authentication)"""

    def authenticate(self, username, password):
        """
        Test authentication - accepts any username/password
        Useful for development and testing
        """
        try:
            # Check if user exists
            user = User.query.filter_by(username=username).first()

            if not user:
                # Create test user if doesn't exist
                user = User(
                    username=username,
                    email=f"{username}@maersk.com",
                    full_name=f"Test User {username}",
                    department="Testing",
                    is_active=True
                )
                db.session.add(user)
                db.session.commit()
                logger.info(f"Created test user: {username}")

            if not user.is_active:
                return {'error': 'User account is inactive'}, 401

            return {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name
            }, 200

        except Exception as e:
            logger.error(f"Test auth error: {e}")
            return {'error': 'Authentication failed'}, 500

    def get_user_info(self, user_id):
        """Get user information"""
        try:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {'error': 'Failed to get user info'}, 500


class LDAPAuthProvider(AuthProvider):
    """LDAP authentication provider for Maersk"""

    def __init__(self):
        try:
            import ldap
            self.ldap = ldap
        except ImportError:
            logger.warning("python-ldap not installed. LDAP auth will fail.")
            self.ldap = None

    def authenticate(self, username, password):
        """
        Authenticate against LDAP server (Maersk)
        """
        if not self.ldap:
            return {'error': 'LDAP not configured'}, 500

        try:
            # Connect to LDAP server
            server = current_app.config['LDAP_SERVER']
            base_dn = current_app.config['LDAP_BASE_DN']
            user_dn = current_app.config['LDAP_USER_DN']

            # Construct full DN
            full_dn = f"uid={username},{user_dn},{base_dn}"

            # Connect and bind
            conn = self.ldap.initialize(server)
            conn.simple_bind_s(full_dn, password)

            # Get user information from LDAP
            search_filter = f"(uid={username})"
            result = conn.search_s(user_dn, self.ldap.SCOPE_SUBTREE, search_filter)

            if not result:
                return {'error': 'User not found in LDAP'}, 401

            # Extract user info
            ldap_user_data = result[0][1]
            email = ldap_user_data.get(b'mail', [b''])[0].decode('utf-8')
            full_name = ldap_user_data.get(b'displayName', [b''])[0].decode('utf-8')
            department = ldap_user_data.get(b'departmentNumber', [b''])[0].decode('utf-8')

            # Check/create user in database
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(
                    username=username,
                    email=email or f"{username}@maersk.com",
                    full_name=full_name or username,
                    department=department,
                    is_active=True
                )
                db.session.add(user)
                db.session.commit()
                logger.info(f"Created LDAP user: {username}")
            else:
                # Update user info
                user.email = email or user.email
                user.full_name = full_name or user.full_name
                user.department = department or user.department
                db.session.commit()

            conn.unbind_s()

            return {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'department': user.department
            }, 200

        except self.ldap.INVALID_CREDENTIALS:
            logger.warning(f"Invalid LDAP credentials for user: {username}")
            return {'error': 'Invalid credentials'}, 401
        except Exception as e:
            logger.error(f"LDAP auth error: {e}")
            return {'error': 'Authentication failed'}, 500

    def get_user_info(self, user_id):
        """Get user information"""
        try:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {'error': 'Failed to get user info'}, 500


class OAuthAuthProvider(AuthProvider):
    """OAuth authentication provider"""

    def authenticate(self, token):
        """Authenticate using OAuth token"""
        # This would typically validate the token against OAuth provider
        pass

    def get_user_info(self, user_id):
        """Get user information"""
        pass


class SAMLAuthProvider(AuthProvider):
    """SAML authentication provider"""

    def authenticate(self, saml_response):
        """Authenticate using SAML response"""
        # This would typically validate SAML response
        pass

    def get_user_info(self, user_id):
        """Get user information"""
        pass


def get_auth_provider():
    """Get authentication provider based on configuration"""
    auth_type = current_app.config.get('AUTH_TYPE', 'test').lower()

    providers = {
        'test': TestAuthProvider,
        'ldap': LDAPAuthProvider,
        'oauth': OAuthAuthProvider,
        'saml': SAMLAuthProvider,
    }

    provider_class = providers.get(auth_type, TestAuthProvider)
    return provider_class()


def create_tokens(user_id, username):
    """Create JWT tokens for authenticated user"""
    try:
        access_token = create_access_token(
            identity=str(user_id),
            additional_claims={'user_id': user_id, 'username': username}
        )
        refresh_token = create_refresh_token(
            identity=str(user_id),
            additional_claims={'user_id': user_id, 'username': username}
        )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200
    except Exception as e:
        logger.error(f"Token creation error: {e}")
        return {'error': 'Failed to create tokens'}, 500


def log_audit(user_id, action, resource_type, resource_id=None, details=None):
    """Log user action to audit trail"""
    try:
        from models import AuditLog
        from flask import request

        audit = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(audit)
        db.session.commit()
    except Exception as e:
        logger.error(f"Audit logging error: {e}")
