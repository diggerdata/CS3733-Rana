from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime

from ..models import Schedule
from .. import db

schedule_blueprint = Blueprint('schedule', __name__)

class ScheduleAPI(MethodView):
    def get(self, schedule_id):
        return make_response(schedule_id), 201
    def post(self):
        """Create a new schedule."""
        post_data = request.get_json()
        print(post_data.get('name'))
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
                db.session.commit()
                resp = {
                    'status': 'success',
                    'message': 'Successfully created schedule.'
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