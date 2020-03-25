from flask import Flask
from api import api

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/'):
    return 'hi'

if __name__ == "__main__":
    main()