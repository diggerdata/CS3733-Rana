from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime, timedelta

from ..models import Schedule, User, TimeSlot, Meeting
from .. import db

sysadmin_blueprint = Blueprint('sysadmin', __name__)

class SysAdminAPI(MethodView):
    def delete(self):
        sent_secret_code = None
        if 'Authorization' in request.headers:
            sent_secret_code = request.headers.get('Authorization')
        else:
            resp = {
                'status': 'fail',
                'message': 'Authorization failed. Please provide a secret code.'
            }
            return make_response(jsonify(resp)), 401
        user = User.query.filter_by(secret_code=sent_secret_code).first()
        if user and user.user_type == 'sysadmin':
            if 'days' in request.args:
                now = datetime.utcnow()
                num_days = int(request.args.get('days'))
                date = now - timedelta(days=num_days)
                schedules = Schedule.query.filter(Schedule.created <= date).all()
                num_schedules = len(schedules)
                for schedule in schedules:
                    timeslots = TimeSlot.query.with_parent(schedule).all()
                    for timeslot in timeslots:
                        meeting = Meeting.query.with_parent(timeslot).first()
                        if meeting:
                            db.session.delete(meeting)
                    TimeSlot.query.with_parent(schedule).delete(synchronize_session=False)
                Schedule.query.filter(Schedule.created.between(date, datetime.utcnow())).delete(synchronize_session=False)
                db.session.commit()
                resp = {
                    'status': 'success',
                    'message': 'Schedules deleted.',
                    'num_deleted': num_schedules
                }
                return make_response(jsonify(resp)), 201
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Please provide a number of days.'
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Authorization failed. Secret code is incorrect.'
            }
            return make_response(jsonify(resp)), 401

    def get(self):
        sent_secret_code = None
        if 'Authorization' in request.headers:
            sent_secret_code = request.headers.get('Authorization')
        else:
            resp = {
                'status': 'fail',
                'message': 'Authorization failed. Please provide a secret code.'
            }
            return make_response(jsonify(resp)), 401
        user = User.query.filter_by(secret_code=sent_secret_code).first()
        if user and user.user_type == 'sysadmin':
            if 'hours' in request.args:
                now = datetime.utcnow()
                num_hours = int(request.args.get('hours'))
                date = now - timedelta(hours=num_hours)
                schedules = Schedule.query.filter(Schedule.created.between(date, now)).all() 
                resp = {
                    'num_created': len(schedules),
                    'schedules': [{
                        'name': s.name,
                        'organizer': s.user.username,
                        'created': s.created.isoformat(),
                    } for s in schedules]
                }
                return make_response(jsonify(resp)), 201
            else:
                resp = {
                    'status': 'fail',
                    'message': 'Please provide a number of hours.'
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Authorization failed. Secret code is incorrect.'
            }
            return make_response(jsonify(resp)), 401

class SysAdminAuthAPI(MethodView):
    def get(self):
        sent_secret_code = None
        sys_admin = None
        if 'Authorization' in request.headers:
            sent_secret_code = request.headers.get('Authorization')
            sys_admin = User.query.filter_by(secret_code=sent_secret_code).first()
            if sys_admin and sys_admin.user_type == 'sysadmin':
                resp = {
                    'authorized': True
                }
                return make_response(jsonify(resp)), 201
            else:
                resp = {
                    'authorized': False
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                'status': 'fail',
                'message': 'Authorization failed. Please provide a secret code.'
            }
            return make_response(jsonify(resp)), 401

sysadmin_view = SysAdminAPI.as_view('sysadmin')
sysadmin_auth_view = SysAdminAuthAPI.as_view('sysadmin_auth')

# add rules for API endpoints
sysadmin_blueprint.add_url_rule(
    '/sysadmin',
    view_func=sysadmin_view,
    methods=['DELETE', 'GET']
)
sysadmin_blueprint.add_url_rule(
    '/sysadmin/authenticate',
    view_func=sysadmin_view,
    methods=['GET',]
)
