# chatbot_factory/routes/auth_routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_babel import gettext as _
from chatbot_factory import db
from chatbot_factory.models import User, Bot
from chatbot_factory.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            active=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Your account has been created! You are now able to log in.'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=_('Register'), form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))
        else:
            flash(_('Login Unsuccessful. Please check email and password.'), 'danger')
    return render_template('login.html', title=_('Login'), form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    bots = Bot.query.filter_by(owner=current_user).order_by(Bot.created_at.desc()).all()
    return render_template('dashboard.html', title=_('Dashboard'), bots=bots)