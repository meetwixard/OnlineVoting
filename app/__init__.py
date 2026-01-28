from flask import Flask
from .models import db
from .config import config_setup
from .routes import vote_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration based on environment
    app.config.from_object(config_setup[config_name])

    db.init_app(app)

    with app.app_context():
        # Ensure tables are created
        db.create_all()

    # Register blueprints (your routes)
    app.register_blueprint(vote_bp)

    return app
