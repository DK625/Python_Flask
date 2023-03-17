from datetime import datetime

from sqlalchemy.orm import deferred

from ..config.connect_db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # password = deferred(db.Column(db.String(100), nullable=False))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100))
    role_id = db.Column(db.String(100))
    # phonenumber = db.Column(db.String(10))
    # positionId = db.Column(db.String(10))
    # image = db.Column(db.String(10))
    createdAt = db.Column(db.DateTime, default=datetime.now)
    # db.Column(db.DateTime, default=datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, email, password, first_name, last_name, address, gender, role_id):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.gender = gender
        self.role_id = role_id
