from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from ..config.connect_db import db
from ..config.marsh_mallow import user_schema
from ..models.model import User

users_schema = user_schema(many=True)


def handle_user_login(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return {"id": user.id, "role_id": user.role_id, "err_code": 0, "err_message": "Login success"}
            return {"err_code": 3, "err_message": "Wrong password"}
        return {"err_code": 2, "err_message": "User not found"}
    except IndentationError:
        return {"err_message": "Can not handle login!"}


def create_new_user(data, role):
    if (
        data
        and ("email" in data)
        and ("password" in data)
        and ("first_name" in data)
        and ("last_name" in data)
        and ("address" in data)
    ):
        email = data["email"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        address = data["address"]
        gender = data["gender"] if ("gender" in data) else None
        role_id = data["role_id"] if ("role_id" in data) else None  # None = null
        try:
            if role != "admin":
                return {"role_id": role, "err_code": 2, "err_message": "not allowed to create new user"}
            user = User.query.filter_by(email=email).first()
            if user:
                return {"err_code": 1, "err_message": "Your email is already in used, plz try another email!"}
            password = generate_password_hash(password, method="sha256")
            new_user = User(email, password, first_name, last_name, address, gender, role_id)
            db.session.add(new_user)
            db.session.commit()
            return {"role_id": role, "err_code": 0, "err_message": "OK"}
        except IndentationError:
            db.session.rollback()
            return {"err_message": "Can not add user!"}
    else:
        return {"err_code": 2, "err_message": "Missing required parameters!"}


def get_all_users(data):
    if data["role_id"] == "admin":
        users = User.query.all()
        return users_schema.dump(users)
    user = User.query.filter_by(id=data["id"]).all()
    return users_schema.dump(user)


def update_user_data(data, currentUser):
    try:
        if currentUser["role_id"] != "admin" and currentUser["id"] != data["id"]:
            return {
                "role_id": currentUser["role_id"],
                "current_id": currentUser["id"],
                "id": data["id"],
                "err_code": 2,
                "err_message": "not allowed to edit other user",
            }
        user = User.query.filter_by(id=data["id"]).first()
        if user:
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.address = data["address"]
            db.session.commit()
            return {"err_code": 0, "err_message": "Update succeeds"}
        return {"err_code": 1, "err_message": "User is not found!"}
    except IndentationError:
        db.session.rollback()
        return {"err_message": "Can not edit user!"}


def delete_user(id, currentUser):
    try:
        if currentUser["role_id"] != "admin" and currentUser["id"] != id:
            return {
                "role_id": currentUser["role_id"],
                "currentId": currentUser["id"],
                "id": id,
                "err_code": 2,
                "err_message": "not allowed to delete other user",
            }
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"err_code": 0, "err_message": "The user is deleted"}
        return {"err_code": 2, "err_message": "The user is not exist"}
    except IndentationError:
        db.session.rollback()
        return {"err_message": "Can not delete user!"}
