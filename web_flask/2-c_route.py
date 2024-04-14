#!/usr/bin/python3
""" 2. Script to start a Flask web application with 3 view functions """

from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def Hello_worlddd():
    """ Returns some text. """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hi():
    """ Return other text. """
    return 'HBNB'


@app.route('/c/<text>')
def lang_c_text(text):
    """ replace text with variable. """
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
