# chatbot_factory/routes/admin_routes.py
import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_babel import gettext as _
from .. import db
from ..models import User, Bot, AdminBroadcast
from ..utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        ADMIN_USER = os.environ.get('ADMIN_USERNAME')
        ADMIN_PASS = os.environ.get('ADMIN_PASSWORD')
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            flash(_('Successfully logged in as admin.'), 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash(_('Invalid credentials. Please try again.'), 'danger')
            return redirect(url_for('admin.login'))
            
    return render_template('admin/login.html', title=_('Admin Login'))

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash(_('You have been logged out.'), 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    user_count = User.query.count()
    bot_count = Bot.query.count()
    broadcasts_count = AdminBroadcast.query.count()
    return render_template('admin/dashboard.html', title=_('Admin Dashboard'), 
                         user_count=user_count, bot_count=bot_count, broadcasts_count=broadcasts_count)

@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', title=_('Manage Users'), users=all_users)

@admin_bp.route('/broadcasts', methods=['GET', 'POST'])
@admin_required
def broadcasts():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        target_plan = request.form.get('target_plan')
        
        if title and content:
            broadcast = AdminBroadcast(
                title=title,
                content=content,
                target_plan=target_plan if target_plan and target_plan != 'all' else None
            )
            db.session.add(broadcast)
            db.session.commit()
            flash(_('New broadcast has been created.'), 'success')
        else:
            flash(_('Please fill in all required fields.'), 'error')
            
        return redirect(url_for('admin.broadcasts'))
        
    all_broadcasts = AdminBroadcast.query.order_by(AdminBroadcast.created_at.desc()).all()
    subscription_plans = ['basic', 'standard', 'premium']
    return render_template('admin/broadcasts.html', title=_('Broadcasts'), 
                         broadcasts=all_broadcasts, plans=subscription_plans)