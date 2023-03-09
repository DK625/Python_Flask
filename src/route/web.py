from flask import Blueprint
from ..controllers import userController
initRouteWeb = Blueprint("initRouteWeb", __name__)


@initRouteWeb.route("/", methods=['GET'])
def handleLogins():
    return "testhomepage"


@initRouteWeb.route("/api/login", methods=['POST'])
def handleLogin():
    return userController.handleLoging()


@initRouteWeb.route("/api/users", methods=['GET'])
def handleGetUsers():
    return userController.handleGetAllUsers()


@initRouteWeb.route("/api/users", methods=['POST'])
def handleCreateNewUsers():
    return userController.handleCreateNewUsers()


@initRouteWeb.route("/api/users", methods=['PUT'])
def handleEditUsers():
    return userController.handleEditUsers()


@initRouteWeb.route("/api/users", methods=['DELETE'])
def handleDeleteUsers():
    return userController.handleDeleteUsers()
