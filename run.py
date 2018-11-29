from rana import app, db
from flask import Flask, request, render_template, Blueprint

# sites
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/schedule')
def c_schedule():
    return render_template('schedule.html')

# @app.route('/schedule/<schedule_id>', methods=['POST'])
# def r_schedule(schedule_id):
#     return render_template('schedule.html', schedule_id=schedule_id)


def reviewschedule():
    return render_template('schedule.html')


@app.route('/createmeeting')
def createmeeting():
    return render_template('createmeeting.html')

# @app.route('/reviewschedule')
# def reviewschedule():
#     return render_template('reviewschedule.html')

@app.route('/sysadmin')
def sysadmin():
    return render_template('sysadmin.html')

@app.route("/sysadmin", methods=['POST'])
def sysadmin_login(): 
    return render_template('sysadmin.html', secretCode=request.form['secretCode'])

if __name__ == '__main__':
    db.create_all()
    app.run(host='localhost', port=5000)

