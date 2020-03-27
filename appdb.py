import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
POSTGRES = {
    'user': 'jkwuser',
    'pw': 'a-nice-random-password',
    'db': 'skudb',
    'host': '10.0.0.46',
    'port': '11366',
}


app = Flask(__name__,template_folder='assets/templates',static_url_path='', static_folder='assets')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
"""
from . import auth, routes, auth_routes, funnel_stats

app.register_blueprint(routes.main_bp)
app.register_blueprint(auth.auth_bp)
app.register_blueprint(auth_routes.oauth_bp)
app.register_blueprint(funnel_stats.metrics_bp)
"""
import flask_home
import models
