from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime

from ..models import Schedule, User, TimeSlot
from .. import db

schedule_blueprint = Blueprint('schedule', __name__)

class ScheduleAPI(MethodView):
    def get(self, schedule_id):
        """Get a schedule by a schedule ID."""
        schedule = Schedule.query.filter_by(id=schedule_id).first()
        if schedule:
            resp = {
                'name': schedule.name,
                'timeslots': [{
                        'id': ts.id, 
                        'start_date': ts.start_date, 
                        'duration': ts.duration, 
                        'available': ts.available
                    } for ts in Schedule.query.filter_by(id=schedule.id).first().timeslots]
            }
            return make_response(jsonify(resp)), 201
        else:
            resp = {
                'status': 'fail',
                'message': 'Schedule does not exist.',
            }
            return make_response(jsonify(resp)), 202
    def post(self):
        """Create a new schedule."""
        post_data = request.get_json()
        schedule = Schedule.query.filter_by(name=post_data.get('name')).first()
        if not schedule:
            try:
                schedule = Schedule(
                    name=post_data.get('name'),
                    start_date=datetime.strptime(post_data.get('start_date'), '%Y-%m-%dT%H:%M:%S.%fZ'),
                    end_date=datetime.strptime(post_data.get('end_date'), '%Y-%m-%dT%H:%M:%S.%fZ'),
                    duration=post_data.get('duration')
                )
                db.session.add(schedule)
                user = User.query.filter_by(username=post_data.get('username'),
                                            user_type='organizer').first()
                if not user:
                    user = User(
                        username=post_data.get('username'),
                        email=post_data.get('email'),
                        user_type='organizer'
                    )
                    db.session.add(user)
                db.session.commit()
                print(schedule.timeslots)
                resp = {
                    'status': 'success',
                    'message': 'Successfully created schedule.',
                    'schedule_id': schedule.id,
                    'secret_code': schedule.secret_code,
                    'start_time': schedule.start_date.hour,
                    'end_time': schedule.end_date.hour,
                    'start_weekday': schedule.start_date.weekday(),
                    'duration': schedule.duration,
                    'timeslots': [{
                        'id': ts.id, 
                        'start_date': ts.start_date, 
                        'duration': ts.duration, 
                        'available': ts.available
                    } for ts in Schedule.query.filter_by(id=schedule.id).first().timeslots]
                }
                return make_response(jsonify(resp)), 201
            except Exception as e:
                print(e)
                resp = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Schedule already exists. Please choose a new name.',
            }
            return make_response(jsonify(resp)), 202

schedule_view = ScheduleAPI.as_view('schedule')

# add Rules for API Endpoints
schedule_blueprint.add_url_rule(
    '/schedule/',
    view_func=schedule_view,
    methods=['POST',]
)
schedule_blueprint.add_url_rule(
    '/schedule/<string:schedule_id>',
    view_func=schedule_view,
    methods=['GET',]
)