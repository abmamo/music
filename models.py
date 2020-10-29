from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, confirmed=False):
        self.email = email
        self.password = generate_password_hash(password)

    def update_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default=None, nullable=True)
    mp3_filename = db.Column(db.String, default=None, nullable=True)
    mp3_url = db.Column(db.String, default=None, nullable=True)
    webm_filename = db.Column(db.String, default=None, nullable=True)
    webm_url = db.Column(db.String, default=None, nullable=True)
    published = db.Column(db.Boolean, default=False, nullable=False)