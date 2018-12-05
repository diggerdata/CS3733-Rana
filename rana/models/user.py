from .. import db
from ..common import secret_key

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)
    secret_code = db.Column(db.String(255), nullable=True)

    def __init__(self, username, email, user_type):
        self.username = username
        self.email = email
        self.user_type = user_type
        if self.user_type == 'sysadmin':
            self.secret_code = secret_key()

    def __repr__(self):
        return '<User {}>'.format(self.username)