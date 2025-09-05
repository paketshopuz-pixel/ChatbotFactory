# chatbot_factory/__init__.py
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel

# Configure logging for better debugging
logging.basicConfig(level=logging.DEBUG)

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'
babel = Babel()

def create_app():
    """Application factory pattern implementation"""
    app = Flask(__name__)

    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SESSION_SECRET", "default-dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            'pool_pre_ping': True,
            "pool_recycle": 300,
        },
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=3600,
    )

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_gettext():
        """Make gettext available in templates"""
        def _(text):
            return text
        return dict(_=_)

    # Register blueprints
    from .routes.main_routes import main_bp
    from .routes.auth_routes import auth_bp
    from .routes.bots_routes import bots_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bots_bp)

    # Create database tables
    with app.app_context():
        from . import models  # Import models to ensure they're registered
        db.create_all()
        logging.info("Database tables created successfully")

    return app