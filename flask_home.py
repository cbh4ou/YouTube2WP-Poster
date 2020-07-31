    # A very simple Flask Hello World app for you to get started with...
from flask import Blueprint, render_template, redirect
from flask_login import login_required

home = Blueprint('home', __name__,
                    template_folder='assets/templates',
                    static_folder='assets')

@home.route('/')
@login_required
def route_home():

    return render_template("editor_channels.html")

@home.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve logged in Dashboard."""
    return redirect("/")
    """
    return render_template('dashboard.html',
                           title='Flask-Login Tutorial.',
                           template='dashboard-template',
                           current_user=current_user,
                           body="You are now logged in!")
    """
