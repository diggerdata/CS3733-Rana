from ..app import db

class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    secret_code = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, user):
        self.user = user