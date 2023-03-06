from flask import Blueprint
# from .services import (add_controller_service, get_controller_by_id_service,
#                        get_all_controller_service, update_controller_by_id_service,
#                        delete_controller_by_id_service, get_controller_by_author_service)
controller = Blueprint("controller", __name__)


@controller.route("/")
def add_controller():
    return "ALL USER"


# @controller.route("/management/<int:id>", methods=['GET'])
# def get_controller_by_id(id):
#     return get_controller_by_id_service(id)

# # get all controller


# @controller.route("/controller-management/controller", methods=['GET'])
# def get_all_controller():
#     return get_all_controller_service()

# # update controller


# @controller.route("/controller-management/controller/<int:id>", methods=['PUT'])
# def update_controller_by_id(id):
#     return update_controller_by_id_service(id)

# # delete controller


# @controller.route("/controller-management/controller/<int:id>", methods=['DELETE'])
# def delete_controller_by_id(id):
#     return delete_controller_by_id_service(id)

# # get controller by author


# @controller.route("/controller-management/controller/<string:author>", methods=['GET'])
# def get_controller_by_author(author):
#     return get_controller_by_author_service(author)
