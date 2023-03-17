from .connect_db import ma


class user_schema(ma.Schema):
    class Meta:
        fields = ("id", "email", "first_name", "last_name", "address", "role_id")
