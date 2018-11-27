from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

foo_blueprint = Blueprint('foo', __name__)

class Foo(MethodView):
    def get(self, foo_id):
        return make_response("<h1>HELLO FREEKING WORLD! {}</h1>".format(foo_id)), 201
    def post(self):
        pass

foo_view = Foo.as_view('foo')

# add Rules for API Endpoints
foo_blueprint.add_url_rule(
    '/foo/<string:foo_id>',
    view_func=foo_view,
    methods=['POST', 'GET']
)