from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime, timedelta

from ..models import Schedule, User, TimeSlot, Meeting
from .. import db

meeting_blueprint = Blueprint('meeting', __name__)

class MeetingAPI(MethodView):
    def get(self, schedule_id, secret_code):
        """Get a meeting from a secret code and schedule id."""
        schedule = Schedule.query.filter_by(id=schedule_id).first()
        if schedule:
            meeting = Meeting.query.filter_by(secret_code=secret_code).first()
            if meeting:
                user = User.query.with_parent(meeting).first()
                resp = {
                    'email': user.email,
                    'username': user.username,
                    'user_type': user.user_type,
                    'meeting_id': meeting.id
                }
                return make_response(jsonify(resp)), 201
            else:
                resp = {
                    'status': 'fail',
                    'message': 'No meeting for secret code {}.'.format(secret_code),
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Schedule does not exist.',
            }
            return make_response(jsonify(resp)), 401
    
    def post(self, schedule_id, timeslot_id):
        """Create a meeting in a timeslot."""
        post_data = request.get_json()
        schedule = Schedule.query.filter_by(id=schedule_id).first()
        if schedule:
            timeslot = TimeSlot.query.with_parent(schedule).filter_by(id=timeslot_id).first()
            if timeslot:
                if timeslot.available:
                    user = User.query.filter_by(username=post_data.get('username'),
                                            user_type='participant').first()
                    try:
                        if not user:
                            user = User(
                                username=post_data.get('username'),
                                email=post_data.get('email'),
                                user_type='partipant'
                            )
                            db.session.add(user)
                        meeting = Meeting()
                        db.session.add(meeting)
                        timeslot.meetings.append(meeting)
                        timeslot.available = False
                        user.meetings.append(meeting)
                        db.session.commit()
                        resp = {
                            'status': 'success',
                            'message': 'Meeting created.',
                            'secret_code': meeting.secret_code
                        }
                        return make_response(jsonify(resp)), 201
                    except Exception as e:
                        resp = {
                            'status': 'fail',
                            'message': str(e)
                        }
                        return make_response(jsonify(resp)), 401
                else:
                    resp = {
                        'status': 'fail',
                        'message': 'Meeting not available.',
                    }
                    return make_response(jsonify(resp)), 401
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Timeslot does not exist.',
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Schedule does not exist.',
            }
            return make_response(jsonify(resp)), 401

    def delete(self, schedule_id, timeslot_id):
        """Cancel a meeting by schedule id and timeslot id."""
        schedule = Schedule.query.filter_by(id=schedule_id).first()
        if schedule:
            timeslot = TimeSlot.query.with_parent(schedule).filter_by(id=timeslot_id).first()
            if timeslot:
                meeting = Meeting.query.with_parent(timeslot).first()
                if meeting:
                    sent_secret_code = None
                    if 'Authorization' in request.headers:
                        sent_secret_code = request.headers.get('Authorization')
                    else:
                        resp = {
                            'status': 'fail',
                            'message': 'Authorization failed. Please provide a secret code.'
                        }
                        return make_response(jsonify(resp)), 401
                    if sent_secret_code == meeting.secret_code or sent_secret_code == schedule.secret_code:
                        try:
                            db.session.delete(meeting)
                            timeslot.available = True
                            db.session.commit()
                            resp = {
                                'status': 'success',
                                'message': 'Meeting successfully canceled.'
                            }
                            return make_response(jsonify(resp)), 201
                        except Exception as e:
                            resp = {
                                'status': 'fail',
                                'message': str(e)
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
                        'message': 'Meeting does not exist.',
                    }
                    return make_response(jsonify(resp)), 401
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Timeslot does not exist.',
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Schedule does not exist.',
            }
            return make_response(jsonify(resp)), 401
    
meeting_view = MeetingAPI.as_view('meeting')

# add rules for API endpoints
meeting_blueprint.add_url_rule(
    '/schedule/<int:schedule_id>/timeslot/<int:timeslot_id>',
    view_func=meeting_view,
    methods=['POST', 'DELETE']
)
meeting_blueprint.add_url_rule(
    '/schedule/<int:schedule_id>/meeting/<string:secret_code>',
    view_func=meeting_view,
    methods=['GET',]
)
