from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "User needs to be logged in to view this page!"
login_manager.login_message_category = "warning"

from application import routes