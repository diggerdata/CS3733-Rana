from .. import db

class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id'))
    timeslot = db.relationship('TimeSlot', backref=db.backref('timeslot', lazy=True))
    secret_code = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Meeting %r>' % self.timeslot