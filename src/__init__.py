from flask import Flask, request, Blueprint
from .config.connectDB import db
from .models.model import User
import os
from .config.config import config
from .route.web import initRouteWeb
from flask_cors import CORS


def create_db(app):
    if not os.path.exists("src/src.db"):
        db.init_app(app)
        with app.app_context():
            db.create_all()
        print("Created database!")


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(config)
    CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    create_db(app)
    app.register_blueprint(initRouteWeb)
    return app
