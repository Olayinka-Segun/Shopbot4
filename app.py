from flask import Flask, render_template
from extensions import db, login_manager
from auth.routes import auth_bp
from bot.chat_routes import chat_bp  # Import the chatbot blueprint
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp, url_prefix='/chat')  # Register the chat blueprint with a URL prefix

    return app


# The main entry point of the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('base.html')