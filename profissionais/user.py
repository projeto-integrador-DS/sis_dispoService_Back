from flask_login import UserMixin

class User_profiss(UserMixin):
    def __init__(self, id):
        self.id = id