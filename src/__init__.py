from flask import Flask, request, Blueprint
from .controllers.userController import controller
from .config.connectDB import db
# from .borrow.controller import borrow
# from .extension import db, ma
# from .model import Students, Books, Author, Category, Borrows
from .models.model import User
import os
from .config.config import config
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# db = SQLAlchemy()
# ma = Marshmallow()


def create_db(app):
    if not os.path.exists("src/src.db"):
        db.init_app(app)
        with app.app_context():
            db.create_all()
        print("Created database!")


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(config)
    # db = SQLAlchemy()
    # db.init_app(app)
    # ma.init_app(app)
    # app.config.from_pyfile(config_file)
    create_db(app)
    app.register_blueprint(controller)
    # app.register_blueprint(borrow)
    # print(app.config["SECRET_KEY"])
    # print(app.config["SQLALCHEMY_DATABASE_URI"])
    return app
