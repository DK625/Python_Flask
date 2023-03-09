from .connectDB import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', "firstName",
                  'lastName', 'address', 'roleId')
