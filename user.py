class User:
    def __init__(self, id, username):
        self._id = id
        self._username = username
        self._authenticated = False

    @property
    def auth(self):
        return self._authenticated

    @auth.setter
    def auth(self, auth_stat):
        self._authenticated = auth_stat

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
    