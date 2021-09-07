from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#create app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

from app import routes

#init packages
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

#import Blueprint
#from app.blueprints.user.routes import user

from app import user
from app import auth