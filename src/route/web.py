from flask_restful import Resource

from ..controllers import user_controller


class TodoList(Resource):
    def get(self):
        return "testhomepage"


class User(Resource):
    def get(self):
        return user_controller.handle_get_all_users()

    def post(self):
        return user_controller.handle_create_new_users()

    def put(self):
        return user_controller.handle_edit_users()

    def delete(self):
        return user_controller.handle_delete_users()


class Login(Resource):
    def post(self):
        return user_controller.handle_loging()
