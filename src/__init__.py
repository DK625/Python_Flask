import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from .config.config import config
from .config.connect_db import db
from .route.web import Login, TodoList, User


def create_db(app):
    if not os.path.exists("src/src.db"):
        db.init_app(app)
        with app.app_context():
            db.create_all()
        print("Created database!")


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config.from_mapping(config)

    CORS(app, supports_credentials=True)
    create_db(app)
    api.add_resource(TodoList, "/")
    api.add_resource(Login, "/api/login")
    api.add_resource(User, "/api/users")
    return app
