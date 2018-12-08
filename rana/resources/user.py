from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime, timedelta
from sqlalchemy import Date, cast

from ..models import Schedule, User, TimeSlot
from .. import db

user_blueprint = Blueprint('user', __name__)

class UserAPI(MethodView):
    def get(self, secret_code):
        """Get user information based on a secret code."""
        pass