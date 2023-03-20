import jwt
from flask import current_app, request


def Middleware():
    token = request.headers["Authorization"].split()[1]
    current_user = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    return current_user
