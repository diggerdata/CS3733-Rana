import os

from flask import Flask, Blueprint, render_template
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

from rana.resources import schedule_blueprint

# add blueprints here
app.register_blueprint(schedule_blueprint)

# sites
@app.route('/')
@app.route('/base')
def index():
    return render_template('index.html')

@app.route('/otherview')
def createschedule():
    return render_template('createschedule.html')

