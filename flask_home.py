    # A very simple Flask Hello World app for you to get started with...
import sys
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import json
from appdb import db
from datetime import date, timedelta, datetime
import pandas as pd
import os
from werkzeug.utils import secure_filename
import time
from flask_login import login_required

home = Blueprint('home', __name__,
                    template_folder='assets/templates',
                    static_folder='assets')

@home.route('/')
def test_main():

    return ("<h1>Success</h1>")

