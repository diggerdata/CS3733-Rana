from datetime import datetime
import random
import string

from .timeslot import TimeSlot

from .. import db

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=15)
    secret_code = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name, start_date, end_date, duration):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.secret_code = self.random_str()
    
    def __repr__(self):
        return '<Schedule {}>'.format(self.name)

    def add_timeslots(self, duration):
        """Add all timeslots to schedule based on duration.
        
        Parameters
        ----------
        duration : int
            The individual timeslot duration.
        """

        last_time = self.start_date
        # TODO: Implement

    @staticmethod
    def random_str(length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length)).upper()