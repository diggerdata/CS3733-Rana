from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime, timedelta
from sqlalchemy import Date, cast

from ..models import Schedule, User, TimeSlot
from .. import db

timeslot_blueprint = Blueprint('timeslot', __name__)

class ToggleTimeslotAPI(MethodView):
    def post(self, schedule_id, timeslot_id, toggle):
        """Toggle a timeslot within a schedule."""
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
                timeslot = TimeSlot.query.with_parent(schedule).filter_by(id=timeslot_id).first()
                if timeslot:
                    try:
                        if toggle == 'open':
                            timeslot.available = True
                        elif toggle == 'close':
                            timeslot.available = False
                        else:
                            resp = {
                                'status': 'fail',
                                'message': 'Provide a valid toggle (open, close).'
                            }
                            return make_response(jsonify(resp)), 401
                        db.session.commit()
                        resp = {
                            'status': 'success',
                            'message': 'Timeslot toggled.'
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
                        'message': 'Timeslot does not exist.',
                    }
                    return make_response(jsonify(resp)), 401
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Authorization failed. Secret code is incorrect.'
                }
                return make_response(jsonify(resp)), 401

class ToggleWeekTimeslotAPI(MethodView):
    def post(self, schedule_id, toggle):
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
                if request.args.get('day') and request.args.get('day'):
                    try:
                        day = datetime.strptime(request.args.get('day'), '%Y-%m-%dT%H:%M:%S.%fZ').date()
                        if toggle == 'open':
                            TimeSlot.query.with_parent(schedule).filter(db.func.DATE(TimeSlot.start_date) == day).\
                                update({TimeSlot.available: True}, synchronize_session=False)
                        elif toggle == 'close':
                            TimeSlot.query.with_parent(schedule).filter(db.func.DATE(TimeSlot.start_date) == day).\
                                update({TimeSlot.available: False}, synchronize_session=False)
                        else:
                            resp = {
                                'status': 'fail',
                                'message': 'Provide a valid toggle (open, close).'
                            }
                            return make_response(jsonify(resp)), 401
                        db.session.commit()
                        timeslots = TimeSlot.query.with_parent(schedule).filter(db.func.DATE(TimeSlot.start_date) == day).all()
                        resp = {
                            'status': 'success',
                            'message': 'Timeslot toggled.'
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
                        'message': 'Provide a day to toggle availability.'
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

toggle_timeslot_view = ToggleTimeslotAPI.as_view('toggle_timeslot_api')
toggle_week_timeslot_view = ToggleWeekTimeslotAPI.as_view('toggle_week_timeslot_api')

# add rules for API endpoints
timeslot_blueprint.add_url_rule(
    '/schedule/<string:schedule_id>/timeslot/<int:timeslot_id>/<string:toggle>',
    view_func=toggle_timeslot_view,
    methods=['POST',]
)
timeslot_blueprint.add_url_rule(
    # ?toggle=open or ?toggle=close
    '/schedule/<string:schedule_id>/timeslot/<string:toggle>',
    view_func=toggle_week_timeslot_view,
    methods=['POST',]
)