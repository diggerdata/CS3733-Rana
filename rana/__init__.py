import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Setup flask config to check of on AWS or not
conf = None
if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    conf = 'config.ProductionConfig'
else:
    conf = 'config.DevelopmentConfig'

# import the specified config
app.config.from_object(conf)

# setup the database object
db = SQLAlchemy(app)

from rana.resources import schedule_blueprint, meeting_blueprint, timeslot_blueprint, sysadmin_blueprint

# add blueprints here
app.register_blueprint(schedule_blueprint)
app.register_blueprint(meeting_blueprint)
app.register_blueprint(timeslot_blueprint)
app.register_blueprint(sysadmin_blueprint)

from rana.models import User

sysadmin = User.query.filter_by(user_type='sysadmin').all()
if not sysadmin:
    try:
        sysadmin = User('god', 'god@op.com', 'sysadmin')
        db.session.add(sysadmin)
        db.session.commit()
    except Exception as e:
        print(e)