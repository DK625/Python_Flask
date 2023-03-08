from ..config.connectDB import db
from ..config.marshMallow import UserSchema
from sqlalchemy.sql import func
from ..models.model import User
from werkzeug.security import check_password_hash, generate_password_hash
users_schema = UserSchema(many=True)


def handleUserLogin(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return {
                    "id": user.id,
                    "roleId": user.roleId,
                    "errCode": 0,
                    "errMessage": "Login success"
                }
            return {
                "errCode": 3,
                "errMessage": "Wrong password"
            }
        return {
            "errCode": 2,
            "errMessage": "User not found"
        }
    except IndentationError:
        return {
            "errMesage": "Can not handle login!"
        }


def createNewUser(data, role):
    if (data and ('email' in data) and ('password' in data)
            and ('firstName' in data) and ('lastName' in data) and ('address' in data)):
        email = data['email']
        password = data['password']
        firstName = data['firstName']
        lastName = data['lastName']
        address = data['address']
        gender = data['gender'] if ('gender' in data) else None
        roleId = data['roleId'] if ('roleId' in data) else None  # None = null
        try:
            if (role != "admin"):
                return {
                    "roleId": role,
                    "errCode": 2,
                    "errMessage": "not allowed to create new user"
                }
            user = User.query.filter_by(email=email).first()
            if user:
                return {
                    "errCode": 1,
                    "errMessage": 'Your email is already in used, plz try another email!'
                }
            password = generate_password_hash(password, method="sha256")
            new_user = User(email, password, firstName,
                            lastName, address, gender, roleId)
            db.session.add(new_user)
            db.session.commit()
            return {
                "roleId": role,
                "errCode": 0,
                "errMessage": 'OK'
            }
        except IndentationError:
            db.session.rollback()
            return {
                "errMesage": "Can not add user!"
            }
    else:
        return {
            "errCode": 2,
            "errMessage": "Missing required parameters!"
        }


def getAllUsers(data):
    if (data['roleId'] == "admin"):
        users = User.query.all()
        return users_schema.jsonify(users), 202
    user = User.query.filter_by(id=data['id']).all()
    return users_schema.jsonify(user), 202


def updateUserData(data, currentUser):
    try:
        if (currentUser['roleId'] != "admin" and currentUser['id'] != data['id']):
            return {
                "roleId": currentUser['roleId'],
                "currentId": currentUser['id'],
                "id": data['id'],
                "errCode": 2,
                "errMessage": "not allowed to edit other user"
            }
        user = User.query.filter_by(id=data['id']).first()
        if user:
            user.firstName = data['firstName']
            user.lastName = data['lastName']
            user.address = data['address']
            db.session.commit()
            return {
                "errCode": 0,
                "errMessage": 'Update succeeds'
            }
        return {
            "errCode": 1,
            "errMessage": 'User is not found!'
        }
    except IndentationError:
        db.session.rollback()
        return {
            "errMesage": "Can not edit user!"
        }


def deleteUser(id, currentUser):
    try:
        if (currentUser['roleId'] != "admin" and currentUser['id'] != id):
            return {
                "roleId": currentUser['roleId'],
                "currentId": currentUser['id'],
                "id": id,
                "errCode": 2,
                "errMessage": "not allowed to delete other user"
            }
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {
                "errCode": 0,
                "errMessage": 'The user is deleted'
            }
        return {
            "errCode": 2,
            "errMessage": 'The user is not exist'
        }
    except IndentationError:
        db.session.rollback()
        return {
            "errMesage": "Can not delete user!"
        }
