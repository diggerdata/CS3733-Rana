from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime, timedelta

from ..models import Schedule, User, TimeSlot, Meeting
from .. import db

meeting_blueprint = Blueprint('meeting', __name__)

class MeetingAPI(MethodView):
    def get(self, schedule_id, meeting_id):
        pass
    
    def post(self, schedule_id, timeslot_id):
        """Create a meeting in a timeslot."""
        post_data = request.get_json()
        schedule = Schedule.query_by(id=schedule_id).first()
        if schedule:
            timeslot = TimeSlot.query.with_parent(schedule).query_by(id=timeslot_id).first()
            if timeslot:
                if timeslot.available:
                    user = User.query.filter_by(username=post_data.get('username'),
                                            user_type='participant').first()
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
                    user.meetings.append(meeting)
                    db.session.commit()
                    resp = {
                        'status': 'success',
                        'message': 'Meeting created.',
                        'secret_code': meeting.secret_code
                    }
                    return make_response(jsonify(resp)), 201
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

    def delete(self, schedule_id, meeting_id):
        pass
    
meeting_view = MeetingAPI.as_view('meeting')

# add rules for API endpoints
meeting_blueprint.add_url_rule(
    '/schedule/<string:schedule_id>/timeslot/<string:timeslot_id>',
    view_func=meeting_view,
    methods=['POST',]
)