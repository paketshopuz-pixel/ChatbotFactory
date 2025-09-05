# chatbot_factory/routes/admin_routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required
from flask_babel import gettext as _
from .. import db
from ..models import User, Bot, AdminBroadcast, SubscriptionType
from ..utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    user_count = User.query.count()
    bot_count = Bot.query.count()
    broadcasts_count = AdminBroadcast.query.count()
    return render_template('admin/dashboard.html', title=_('Admin Dashboard'), 
                         user_count=user_count, bot_count=bot_count, broadcasts_count=broadcasts_count)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', title=_('Manage Users'), users=all_users)

@admin_bp.route('/broadcasts', methods=['GET', 'POST'])
@login_required
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
                target_plan=SubscriptionType(target_plan) if target_plan and target_plan != 'all' else None
            )
            db.session.add(broadcast)
            db.session.commit()
            flash(_('New broadcast has been created.'), 'success')
        else:
            flash(_('Please fill in all required fields.'), 'error')
            
        return redirect(url_for('admin.broadcasts'))
        
    all_broadcasts = AdminBroadcast.query.order_by(AdminBroadcast.created_at.desc()).all()
    return render_template('admin/broadcasts.html', title=_('Broadcasts'), 
                         broadcasts=all_broadcasts, plans=SubscriptionType)