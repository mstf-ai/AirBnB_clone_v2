#!/usr/bin/python3
""" 5. Add fifth view func that displays HTML page if n is int """

from flask import Flask
from flask import render_template


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


@app.route('/python/')
@app.route('/python/<text>')
def p_text(text='is cool'):
    """ replace more text with another variable. """
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>')
def n_text(n):
    """ replace with int only if given int. """
    n = str(n)
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def html_num(n):
    """ display html if n is int. """
    n = str(n)
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
