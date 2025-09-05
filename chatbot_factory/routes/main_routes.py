# chatbot_factory/routes/main_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app, abort
from flask_babel import gettext as _
from flask_login import login_required, current_user
from .. import db
from ..models import Bot

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - shows landing page for anonymous users, dashboard for logged in users"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template('index.html')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        
        if not email:
            flash('Email is required.', 'danger')
            return render_template('profile.html')
        
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html')

@main_bp.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html', title=_('Subscriptions'))

@main_bp.route('/download/product_template')
@login_required
def download_template():
    """Download Excel template for bulk product upload"""
    try:
        return send_from_directory(current_app.config['INSTANCE_PATH'], 'product_template.xlsx', as_attachment=True)
    except FileNotFoundError:
        abort(404)