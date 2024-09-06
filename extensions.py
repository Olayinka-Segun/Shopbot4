from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'  # Redirect to login page if the user is not authenticated
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    # Other configurations
    login_manager.init_app(app)
    return app
