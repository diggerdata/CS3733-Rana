from flask import Flask, request, render_template, Blueprint

functionality_blueprint = Blueprint(
    'buttons', __name__,
    template_folder='templates'
)

@functionality_blueprint.route('/schedule')
def c_schedule():
    return render_template('schedule.html')
