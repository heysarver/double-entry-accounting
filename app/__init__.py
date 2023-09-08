
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from dotenv import load_dotenv
from flask_cors import CORS
import os
import psycopg2

load_dotenv()

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
seeder = FlaskSeeder()

def get_db_connection():
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD)
    return conn

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)

    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "").split(",")
    CORS(app, resources={r'*': {'origins': allowed_origins}})

    from app import models, seeds # verify if this is needed for migrating or seeding
    
    from .routes import accounts, transactions, reports
    app.register_blueprint(accounts.bp)
    app.register_blueprint(transactions.bp)
    app.register_blueprint(reports.bp)

    return app
