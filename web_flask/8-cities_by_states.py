#!/usr/bin/python3
""" Starts a Flask web app """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def dis_pose(exception):
    """ Remove current session """
    storage.close()


@app.route('/cities_by_states')
def state_s():
    """ Display list of all the state_s """
    state_s = storage.all(State)
    states__list = list(state_s.values())
    return render_template('8-cities_by_states.html', state_s=states_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
