from .. import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    user_type = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)