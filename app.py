import os
# import flask dependencies
from flask import Flask, abort
# import sqlalchemy for user db management
from flask_sqlalchemy import SQLAlchemy
# import csrf protection
from flask_wtf.csrf import CSRFProtect
# import mail manager
from flask_mail import Mail, Message
# import login manager
from flask_login import LoginManager
# import image upload library
from flask_uploads import UploadSet, configure_uploads
# import serializer for generating tokens
from itsdangerous import URLSafeTimedSerializer
# config
import config
# env manager
from dotenv import load_dotenv
import os
# load env
load_dotenv()
# define app
app = Flask(__name__)
# get environment
environment = os.environ.get("ENVIRONMENT")
# configure application
if environment == "testing":
    app.config.from_object(config.TestingConfig)
elif environment == "production":
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.DevelopmentConfig)
# configure login manager
login_manager = LoginManager()
# define loggin in route
login_manager.login_view = 'player_bp.signin'
login_manager.login_message = "sign in"
login_manager.init_app(app)
# define user loader for flask login
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        abort(500)
# configure csrf
csrf = CSRFProtect(app)
# initialize db
db = SQLAlchemy(app)
# initialize mail
mail = Mail(app)
# configure uploads / define allowed file types
audio = UploadSet('audio', ('mp3', 'wav', 'webm'))
configure_uploads(app, audio)
# initialize serializer with the app secret key
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def send_mail(subject, sender, recipients, text_body):
    """
        mail sending function
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)

from models import User, Song

# create all schema
db.create_all()
# error handlers
from errors import errors_bp as error_module
# register
app.register_blueprint(error_module)
# routes
from routes import player_bp as player_module
# register
app.register_blueprint(player_module)
# admin creation function
from init import create_user
# create admin
create_user(app, environment, User, db)

