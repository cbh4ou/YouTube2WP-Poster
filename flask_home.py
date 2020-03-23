from flask import Flask

app = Flask(__name__)


@app.route('/'):
    return '<h1> hey </h1>'

if __name__ == __main__:
        