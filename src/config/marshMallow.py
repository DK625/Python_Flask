from .connectDB import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', "firstName",
                  'lastName', 'address', 'roleId')
