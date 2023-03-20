import json
from datetime import datetime, timedelta

import jwt
from flask import Flask, current_app, jsonify, request

from ..config.connect_db import db
from ..config.marsh_mallow import user_schema
from ..controllers.verify_and_authorization import Middleware
from ..models.model import User
from ..services import user_service

users_schema = user_schema(many=True)


def handle_loging():
    data = json.loads(request.data)
    if data and ("email" in data) and ("password" in data):
        email = data["email"]
        password = data["password"]
        user_data = user_service.handle_user_login(email, password)
        if user_data["err_code"] == 0:
            token = jwt.encode(
                {
                    "role_id": user_data["role_id"],
                    "id": user_data["id"],
                    "exp": datetime.utcnow() + timedelta(minutes=30000),
                },
                current_app.config["SECRET_KEY"],
            )
            response = jsonify(
                {
                    "token": token,
                    "err_code": user_data["err_code"],
                    "err_message": user_data["err_message"],
                }
            )
            response.status_code = 200
            return response
        response = jsonify(
            {
                "err_code": user_data["err_code"],
                "message": user_data["err_message"],
            }
        )
        response.status_code = 200
        return response
    response = jsonify({"err_code": "1", "message": "Missing inputs parameter!"})
    response.status_code = 404
    return response


def handle_create_new_users():
    data = json.loads(request.data)
    try:
        current_user = Middleware()
        user_data = user_service.create_new_user(data, current_user["role_id"])
        return jsonify(
            {
                "message": user_data,
            }
        )
    except:
        return jsonify(
            {
                "err_message": "not logged in yet",
            }
        )


def handle_get_all_users():
    try:
        data = Middleware()
        if data and ("id" in data) and ("role_id" in data):
            user_data = user_service.get_all_users(data)
            return jsonify({"err_code": 0, "err_message": "OK", "users": user_data})
        return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
    except:
        return jsonify({"err_message": "not logged in yet"})


def handle_edit_users():
    try:
        current_user = Middleware()
        data = json.loads(request.data)
        if (data and ("first_name" in data) and ("last_name" in data) and ("address" in data)) and ("id" in data):
            message = user_service.update_user_data(data, current_user)
            response = jsonify({"message": message})
            response.status_code = 202
            return response
        return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
    except:
        return jsonify({"err_message": "not logged in yet"})


def handle_delete_users():
    try:
        current_user = Middleware()
        data = json.loads(request.data)
        if data and ("role_id" in current_user) and "id" in data:
            message = user_service.delete_user(data["id"], current_user)
            response = jsonify({"message": message})
            response.status_code = 202
            return response
        return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
    except:
        return jsonify({"err_message": "not logged in yet"})
