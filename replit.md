# Overview

ChatBot Factory is a SaaS platform built with Flask that enables users to create, manage, and deploy AI-powered chatbots without requiring coding knowledge. The application follows a modular architecture with clear separation of concerns between authentication, chatbot management, and user profiles. The platform is designed to be scalable and maintainable, with a foundation ready for future AI service integration.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Application Structure
The application uses Flask's Application Factory pattern implemented in `chatbot_factory/__init__.py`, providing a clean and testable architecture. The codebase is organized into distinct modules:

- **Routes**: Blueprints for `main_routes.py` (dashboard, profile, chatbot management) and `auth_routes.py` (login, registration, logout)
- **Models**: SQLAlchemy models for `User` and `ChatBot` entities with proper relationships
- **Forms**: WTForms classes for secure form handling with CSRF protection
- **Services**: Placeholder AI service module for future integration with AI providers
- **Utils**: Utility functions and decorators for common operations

## Authentication & Authorization
- Flask-Login for session management with secure password hashing using Werkzeug
- User registration and login with form validation
- Session-based authentication with remember-me functionality
- CSRF protection enabled globally through WTF-Forms

## Database Design
The application uses SQLAlchemy ORM with Flask-Migrate for database management:

- **User Model**: Stores authentication data (username, email, password hash), profile information (first_name, last_name), and metadata (created_at, updated_at, is_active)
- **ChatBot Model**: Stores chatbot configurations (name, description, system prompt) with timestamps and active status
- Foreign key relationships between users and their chatbots

## Frontend Architecture
- Bootstrap 5 with dark theme for consistent, responsive UI
- Template inheritance system with `base.html` providing common layout
- Form handling with client-side validation and server-side security
- Mobile-responsive design with professional styling

## Configuration Management
- Environment-based configuration using python-dotenv
- Secure session management with configurable secret keys
- Database URL configuration for different environments
- Multi-language support foundation with Flask-Babel

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web framework with SQLAlchemy ORM integration
- **Flask-Login**: User session management and authentication
- **Flask-Migrate**: Database schema versioning and migrations
- **Flask-WTF**: Secure form handling with CSRF protection
- **Flask-Babel**: Internationalization and localization support

## Database
- **SQLAlchemy**: ORM for database operations with PostgreSQL/SQLite support
- **Database URL**: Configurable via environment variable, defaults to SQLite for development

## Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme implementation
- **Bootstrap Icons**: Icon library for UI elements
- **Custom CSS**: Application-specific styling in `static/css/style.css`

## Security & Utilities
- **Werkzeug**: Password hashing and security utilities
- **python-dotenv**: Environment variable management
- **WTForms**: Form validation and rendering with security features

## Planned Integrations
- **AI Service Providers**: Placeholder service module ready for Google Gemini, OpenAI, or other AI API integration
- **Rate Limiting**: Framework prepared for Flask-Limiter implementation
- **Admin Panel**: User role system foundation in place for future admin features