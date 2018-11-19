import os

from flask import Flask, Blueprint
from flask_restful import Api
from rana.resources import Foo

app = Flask(__name__)

# Setup flask config to check of on AWS or not
conf = None
if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    conf = 'config.ProductionConfig'
else:
    conf = 'config.DevelopmentConfig'

app.config.from_object(conf)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Put all API resources here
api.add_resource(Foo, '/Foo', '/Foo/<str:id>')