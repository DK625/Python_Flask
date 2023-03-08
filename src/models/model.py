from ..config.connectDB import db

from datetime import datetime
from sqlalchemy.orm import deferred


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # password = deferred(db.Column(db.String(100), nullable=False))
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100))
    roleId = db.Column(db.String(100))
    # phonenumber = db.Column(db.String(10))
    # positionId = db.Column(db.String(10))
    # image = db.Column(db.String(10))
    createdAt = db.Column(db.DateTime, default=datetime.now)
    # db.Column(db.DateTime, default=datetime.now)
    updatedAt = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, email, password, firstName, lastName, address, gender, roleId):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.gender = gender
        self.roleId = roleId
