import os
import logging
import sys
from flask import Flask, render_template
from models import User
import flask_home, login, routes, commands
from extensions import (
    bcrypt,
    cache,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate
)


POSTGRES = {
    'user': 'jkwuser',
    'pw': 'a-nice-random-password',
    'db': 'skudb',
    'host': 'jkwent-1366.postgres.pythonanywhere-services.com',
    #'host': '10.0.0.46',
    'port': '11366',
}


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__,template_folder='assets/templates',static_url_path='', static_folder='assets')
    app.config.from_object('config.Config')
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = False
    app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jkwuser:a-nice-random-password@jkwent-1366.postgres.pythonanywhere-services.com:11366/skudb'
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    app.app_context().push()
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(login.auth_bp)
    app.register_blueprint(flask_home.home)
    app.register_blueprint(routes.channels)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)





