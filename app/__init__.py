from flask import Flask
import logging
from config import Config
from .extensions import db, migrate, bcrypt, jwt
from .api import register_apis

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register APIs
    register_apis(app)

    # Logging
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    return app