from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

schedule_blueprint = Blueprint('schedule', __name__)

class Schedule(MethodView):
    def get(self, foo_id):
        return make_response("<h1>HELLO FREEKING WORLD! {}</h1>".format(foo_id)), 201
    def post(self):
        """Create a new schedule."""
        post_data = request.get_json()
        pass

foo_view = Schedule.as_view('schedule')

# add Rules for API Endpoints
foo_blueprint.add_url_rule(
    '/schedule/',
    view_func=foo_view,
    methods=['POST',]
)