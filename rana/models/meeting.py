from .. import db
from ..common import secret_key

class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('meetings', lazy=True))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))
    timeslot = db.relationship('TimeSlot', backref=db.backref('meetings', lazy=True))
    secret_code = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self):
        self.secret_code = secret_key()

    def __repr__(self):
        return '<Meeting %r>' % self.timeslot