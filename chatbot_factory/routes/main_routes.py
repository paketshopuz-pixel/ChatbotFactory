# chatbot_factory/routes/main_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import ChatBot

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - shows landing page for anonymous users, dashboard for logged in users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing their chatbots"""
    chatbots = ChatBot.query.filter_by(user_id=current_user.id).order_by(ChatBot.created_at.desc()).all()
    return render_template('dashboard.html', chatbots=chatbots)

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

@main_bp.route('/chatbot/create', methods=['GET', 'POST'])
@login_required
def create_chatbot():
    """Create a new chatbot"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        prompt = request.form.get('prompt')
        
        if not name:
            flash('ChatBot name is required.', 'danger')
            return render_template('create_chatbot.html')
        
        chatbot = ChatBot(
            name=name,
            description=description,
            prompt=prompt,
            user_id=current_user.id
        )
        db.session.add(chatbot)
        db.session.commit()
        flash(f'ChatBot "{chatbot.name}" has been created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('create_chatbot.html')

@main_bp.route('/chatbot/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_chatbot(id):
    """Edit an existing chatbot"""
    chatbot = ChatBot.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        prompt = request.form.get('prompt')
        
        if not name:
            flash('ChatBot name is required.', 'danger')
            return render_template('edit_chatbot.html', chatbot=chatbot)
        
        chatbot.name = name
        chatbot.description = description
        chatbot.prompt = prompt
        db.session.commit()
        flash(f'ChatBot "{chatbot.name}" has been updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_chatbot.html', chatbot=chatbot)

@main_bp.route('/chatbot/<int:id>/delete', methods=['POST'])
@login_required
def delete_chatbot(id):
    """Delete a chatbot"""
    chatbot = ChatBot.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    name = chatbot.name
    db.session.delete(chatbot)
    db.session.commit()
    flash(f'ChatBot "{name}" has been deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))