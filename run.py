from rana import app, db
from flask import Flask, render_template

# sites
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/createschedule')
def createschedule():
    return render_template('createschedule.html')

@app.route('/createmeeting')
def createmeeting():
    return render_template('createmeeting.html')

@app.route('/reviewschedule')
def reviewschedule():
    return render_template('reviewschedule.html')

@app.route('/sysadmin')
def sysadmin():
    return render_template('sysadmin.html')

if __name__ == '__main__':
    db.create_all()
    app.run(host='localhost', port=5000)

