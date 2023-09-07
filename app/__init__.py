
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
seeder = FlaskSeeder()

def create_app(config_class=Config):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)

    # Configure CORS
    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "").split(",")
    CORS(app, resources={r'*': {'origins': allowed_origins}})

    # Import and register Blueprints
    from app import models, seeds
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
