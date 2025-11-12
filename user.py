from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False
    