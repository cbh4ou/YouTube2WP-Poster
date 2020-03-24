from flask import Flask
from api import api

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/'):
    return '<h1> hey </h1>'

if __name__ == "__main__":
    main()