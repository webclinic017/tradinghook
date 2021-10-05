import config as CONFIG
from flask import Flask
from flask_login import LoginManager
import os
import logging

#create app
app = Flask(__name__)

# prepare secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from app import routes

#init packages
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

logging.basicConfig(filename=CONFIG.LOGFILE, level=logging.INFO)

from app import user
from app import auth

#init and create database if necessary
from app import user_db
user_db.init_db()