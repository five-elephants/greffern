import flask_login

class DefaultUser(flask_login.UserMixin):
    def get_id(self):
        return '95be498d714cd297fd89fffcdef7f2e4eed5faa5' 
