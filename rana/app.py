import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from rana.resources import foo_blueprint

app = Flask(__name__)
CORS(app)

# Setup flask config to check of on AWS or not
conf = None
if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    conf = 'config.ProductionConfig'
else:
    conf = 'config.DevelopmentConfig'

app.config.from_object(conf)

db = SQLAlchemy(app)

# add blueprints here
app.register_blueprint(foo_blueprint)
