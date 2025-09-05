# chatbot_factory/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_babel import gettext as _
from .models import User, PlatformType

class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(_('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_('Sign Up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('That username is taken. Please choose a different one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('That email is already registered.'))

class LoginForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember = BooleanField(_('Remember Me'))
    submit = SubmitField(_('Login'))

class BotForm(FlaskForm):
    name = StringField(_('Bot Name'), validators=[DataRequired(), Length(min=3, max=100)])
    platform_type = SelectField(_('Platform'), 
                                choices=[(p.name, p.value.capitalize()) for p in PlatformType],
                                validators=[DataRequired()])
    telegram_token = StringField(_('Telegram Bot Token'))
    submit = SubmitField(_('Save Bot'))

class KnowledgeBaseForm(FlaskForm):
    title = StringField(_('Title (e.g., "Product Price" or "Return Policy")'), validators=[DataRequired(), Length(max=200)])
    content = TextAreaField(_('Content (The information the bot should know)'), validators=[DataRequired()])
    submit = SubmitField(_('Save Entry'))