from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime, timedelta

from ..models import Schedule, User, TimeSlot
from .. import db

schedule_blueprint = Blueprint('schedule', __name__)

class ScheduleAPI(MethodView):
    def get(self, schedule_id):
        """Get the first week of the given schedule, or the week of the given monday date."""
        if schedule_id:
            schedule = Schedule.query.filter_by(id=schedule_id).first()
            if schedule:
                timeslots = None
                if request.args.get('week'):
                    start_time = datetime.strptime(request.args.get('week'), '%Y-%m-%dT%H:%M:%S.%fZ')
                    end_time = start_time + timedelta(days=5)
                    timeslots = TimeSlot.query.with_parent(schedule).filter(TimeSlot.start_date.between(start_time, end_time)).all()
                else:
                    start_time = schedule.start_date
                    end_time = start_time + timedelta(days=(5-start_time.weekday()))
                    timeslots = TimeSlot.query.with_parent(schedule).filter(TimeSlot.start_date.between(start_time, end_time)).all()
                resp = {
                    'status': 'success',
                    'name': schedule.name,
                    'start_time': schedule.start_date.hour,
                    'end_time': schedule.end_date.hour,
                    'start_weekday': schedule.start_date.weekday(),
                    'duration': schedule.duration,
                    'timeslots': [{
                            'id': ts.id, 
                            'start_date': ts.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), 
                            'duration': ts.duration, 
                            'available': ts.available
                        } for ts in timeslots]
                }
                return make_response(jsonify(resp)), 201
                
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Schedule does not exist.',
                }
                return make_response(jsonify(resp)), 401
        else:
            # TODO: Implement report activity (sysadmin)
            pass

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
                user.schedules.append(schedule)
                db.session.commit()
                resp = {
                    'status': 'success',
                    'message': 'Successfully created schedule.',
                    'schedule_id': schedule.id,
                    'secret_code': schedule.secret_code
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
            return make_response(jsonify(resp)), 401

    def delete(self, schedule_id):
        """Delete a schedule by id, requires authorization."""
        if schedule_id:
            schedule = Schedule.query.filter_by(id=schedule_id).first()
            if schedule:
                sent_secret_code = None
                if 'Authorization' in request.headers:
                    sent_secret_code = request.headers.get('Authorization')
                else:
                    resp = {
                        'status': 'fail',
                        'message': 'Authorization failed. Please provide a secret code.'
                    }
                    return make_response(jsonify(resp)), 401
                if sent_secret_code == schedule.secret_code:
                    try:
                        TimeSlot.query.with_parent(schedule).delete(synchronize_session=False)
                        db.session.delete(schedule)
                        db.session.commit()
                        resp = {
                            'status': 'successs',
                            'message': 'Schedule successfully deleted.'
                        }
                        return make_response(jsonify(resp)), 201
                    except Exception as e:
                        resp = {
                            'status': 'fail',
                            'message': e
                        }
                        return make_response(jsonify(resp)), 401
                else:
                    resp = {
                        'status': 'fail',
                        'message': 'Authorization failed. Secret code is incorrect.'
                    }
                    return make_response(jsonify(resp)), 401
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Schedule does not exist.',
                }
                return make_response(jsonify(resp)), 401
        else:
            # TODO: Implement delete old schedules (sysadmin)
            pass

schedule_view = ScheduleAPI.as_view('schedule')

# add rules for API endpoints
schedule_blueprint.add_url_rule(
    '/schedule/',
    view_func=schedule_view,
    methods=['POST', 'DELETE', 'GET']
)
schedule_blueprint.add_url_rule(
    '/schedule/<int:schedule_id>',
    view_func=schedule_view,
    methods=['GET', 'DELETE']
)