import json
from flask import Flask, request, jsonify
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager

from ..models.model import User
from ..config.connectDB import db


from ..services import userService
from flask import current_app


# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta

from ..config.marshMallow import UserSchema
# user_schema = UserSchema()
users_schema = UserSchema(many=True)


def handleLoging():
    data = json.loads(request.data)
    if (data and ('email' in data) and ('password' in data)):
        email = data['email']
        password = data['password']
        userData = userService.handleUserLogin(email, password)
        if (userData['errCode'] == 0):
            # current_app.config['SECRET_KEY'] = "super-secret"
            token = jwt.encode({
                'roleId': userData['roleId'],
                'id': userData['id'],
                'exp': datetime.utcnow() + timedelta(minutes=30000)
            }, current_app.config['SECRET_KEY'])
            return jsonify({
                "token": token,
                "errCode": userData['errCode'],
                "errMessage": userData['errMessage'],
                # "user": userData if userData else {}
            }), 202
        return jsonify({
            "errCode": userData['errCode'],
            "message": userData['errMessage'],
            "user": userData if userData else {}
        }), 202
    return jsonify({
        "errCode": "1",
        "message": "Missing inputs parameter!"
    }), 404


def handleCreateNewUsers():
    data = json.loads(request.data)
    try:
        token = request.headers['Authorization'].split()[1]
        currentUser = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        userData = userService.createNewUser(data, currentUser['roleId'])
        return jsonify(
            userData,
        ), 200
    except:
        return jsonify({
            "errMessage": "not logged in yet",
            # "token": currentUser
        })


def handleGetAllUsers():
    try:
        token = request.headers['Authorization'].split()[1]
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        if (data and ('id' in data) and ('roleId' in data)):
            userData = userService.getAllUsers(data)
            return (
                userData
            )
        return jsonify({
            # "dataUser": data,
            "errCode": "1",
            "errMessage": "Missing inputs parameter!"
        })
    except:
        return jsonify({
            "errMessage": "not logged in yet"
        })


def handleEditUsers():
    try:
        token = request.headers['Authorization'].split()[1]
        currentUser = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        data = json.loads(request.data)
        if (data and ('firstName' in data) and ('lastName' in data) and ('address' in data)) and ('id' in data):
            message = userService.updateUserData(data, currentUser)
            return jsonify(
                message
            ), 202
        return jsonify({
            "errCode": "1",
            "errMessage": "Missing inputs parameter!"
        })
    except:
        return jsonify({
            "errMessage": "not logged in yet"
        })


def handleDeleteUsers():
    try:
        token = request.headers['Authorization'].split()[1]
        currentUser = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        data = json.loads(request.data)
        if (data and ('roleId' in currentUser)):
            message = userService.deleteUser(data['id'], currentUser)
            return jsonify(
                message
            ), 202
        return jsonify({
            "errCode": "1",
            "errMessage": "Missing inputs parameter!"
        })
    except:
        return jsonify({
            "errMessage": "not logged in yet"
        })
