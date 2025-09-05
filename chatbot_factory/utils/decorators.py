# chatbot_factory/utils/decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash, request
from flask_babel import gettext as _

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash(_('You need to be logged in as an admin to access this page.'), 'warning')
            return redirect(url_for('admin.login'))
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