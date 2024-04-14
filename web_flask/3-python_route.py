#!/usr/bin/python3
""" 3. Add third view func that redirects and has default val for variable """

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


@app.route('/python/')
@app.route('/python/<text>')
def p_text(text='is cool'):
    """ replace more text with another variable. """
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
