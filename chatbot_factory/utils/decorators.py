# chatbot_factory/utils/decorators.py
"""
Utility decorators for the application
"""
from functools import wraps
from flask import abort, flash, redirect, url_for, request
from flask_login import current_user

def admin_required(f):
    """
    Decorator that requires user to be an admin
    Note: Admin functionality is not implemented yet, this is a placeholder
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        # TODO: Add admin check when user roles are implemented
        # For now, all authenticated users have access
        
        return f(*args, **kwargs)
    return decorated_function

def ajax_required(f):
    """
    Decorator that requires the request to be made via AJAX
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_xhr:
            abort(400)
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(max_requests=60, per=60):
    """
    Simple rate limiting decorator (placeholder)
    In production, use Flask-Limiter or similar
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO: Implement actual rate limiting
            # This is a placeholder for future implementation
            return f(*args, **kwargs)
        return decorated_function
    return decorator
