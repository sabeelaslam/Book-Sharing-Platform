from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# 1. Initialize extensions globally
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Define where to redirect unauthorized users
login_manager.login_message = 'Please Login First'
login_manager.login_message_category = 'warning'

def create_app():
    app = Flask(
        __name__, 
        template_folder=Config.TEMPLATE_FOLDER,
        static_folder=Config.STATIC_FOLDER,
        static_url_path='/static'
    )
    app.config.from_object(Config)

    # 2. Bind extensions to the app
    db.init_app(app)
    login_manager.init_app(app)

    # 3. Import models so SQLAlchemy knows about them before creating tables
    from app import models 

    # 4. Register routes blueprint
    from .routes.main_routes import bp as main_bp
    app.register_blueprint(main_bp)

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    # 5. Automatically create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app