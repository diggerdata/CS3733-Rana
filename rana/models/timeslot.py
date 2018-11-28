from datetime import datetime

from .. import db

class TimeSlot(db.Model):
    __tablename__ = 'timeslots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    schedule = db.relationship('Schedule', backref=db.backref('timeslots', lazy=True))

    def __repr__(self):
        return '<TimeSlot {}, {}>'.format(self.start_date, self.duration)