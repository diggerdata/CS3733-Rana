from datetime import datetime, timedelta

from .timeslot import TimeSlot

from .. import db
from ..common import secret_key

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=15)
    created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('schedules', lazy=True))
    secret_code = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name, start_date, end_date, duration, hours):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.created = datetime.utcnow()
        self.secret_code = secret_key()
        self.add_timeslots(self.duration, self.start_date, self.end_date, hours)
    
    def __repr__(self):
        return '<Schedule {}>'.format(self.name)

    def add_timeslots(self, duration, start_date, end_date, hours):
        """Add all timeslots to schedule based on duration.
        
        Parameters
        ----------
        duration : int
            The individual timeslot duration.
        """
        last_time = start_date
        delta = timedelta(days=1)
        weekend = set([5, 6])
        # start_time = start_date.hour
        # end_time = end_date.hour
        num = int(hours//(duration/60))
        while last_time <= end_date:
            if last_time.weekday() not in weekend:
                day = last_time
                for i in range(num):
                    is_timeslot = TimeSlot.query.with_parent(self).filter_by(start_date=day).first()
                    if not is_timeslot:
                        timeslot = TimeSlot(
                            start_date=day,
                            duration=duration
                        )
                        self.timeslots.append(timeslot)
                    day += timedelta(minutes=duration)
            last_time += delta
