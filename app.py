import os
# import flask dependencies
from flask import Flask, redirect, render_template, request, url_for, abort
# import to save filename securely
from werkzeug.utils import secure_filename
# import sqlalchemy for user db management
from flask_sqlalchemy import SQLAlchemy
# import password hashing and unhashing libraries
from werkzeug.security import generate_password_hash, check_password_hash
# import csrf protection
from flask_wtf.csrf import CSRFProtect
# import login manager
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user
# import image upload library
from flask_uploads import UploadSet, configure_uploads

# define app
app = Flask(__name__)
# configure application
app.config.from_object('config')
# configure login manager
login_manager = LoginManager()
# define loggin in route
login_manager.login_view = 'signin'
login_manager.init_app(app)
# configure csrf
csrf = CSRFProtect(app)
# initialize db
db = SQLAlchemy(app)
# configure uploads / define allowed file types
audio = UploadSet('audio', ('mp3', 'wav', 'webm'))
configure_uploads(app, audio)

# define user and song schema


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default=None, nullable=True)
    mp3_filename = db.Column(db.String, default=None, nullable=True)
    mp3_url = db.Column(db.String, default=None, nullable=True)
    webm_filename = db.Column(db.String, default=None, nullable=True)
    webm_url = db.Column(db.String, default=None, nullable=True)
    published = db.Column(db.Boolean, default=False, nullable=False)


# create all schema
db.create_all()


# define user loader for flask login
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        abort(500)

# define template routes
@app.route('/', methods=['GET'])
def home():
    try:
        # get only published songs
        songs = Song.query.filter_by(published=True).all()
        return render_template('home.html', songs=songs)
    except:
        abort(404)

# about page route function
@app.route('/about', methods=['GET'])
def about():
    try:
        return render_template('about.html')
    except:
        abort(404)

# AUTHENTICATION
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            # get data from from submitted
            email = request.form['email']
            password = request.form['password']
            # check to see if email exists
            user = User.query.filter_by(email=email).first()
            if user:
                return redirect(url_for('signup'))
            # create new user
            new_user = User(email=email, password=generate_password_hash(
                password, method='sha256'))
            # add user to db
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            # return to login
            return redirect(url_for('signin'))
        return render_template('signup.html')
    except:
        abort(500)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            # get data from form
            email = request.form['email']
            password = request.form['password']
            # query by email
            user = User.query.filter_by(email=email).first()
            # check credentials
            if not user or not check_password_hash(user.password, password):
                return redirect(url_for('signin'))
            # login user using the manager
            login_user(user)
            # redirect to upload page
            return redirect(url_for('cms'))
        return render_template('signin.html')
    except:
        abort(500)


@app.route('/signout')
def signout():
    try:
        # sign out currently logged unser & redirect
        logout_user()
        return redirect(url_for('home'))
    except:
        abort(500)


# CMS
# cms page route function
@app.route('/cms', methods=['GET'])
@login_required
def cms():
    try:
        # get all songs in the database
        songs = Song.query.order_by(Song.id.desc()).all()
        return render_template('cms.html', songs=songs)
    except:
        abort(500)

# delete route functio
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        song = Song.query.filter_by(id=id).first()
        try:
            # remove mp3 and webm files from disk if present
            os.remove(app.config['BASE_DIR'] + url_for('static',
                                                       filename='audio/' + song.webm_filename))
            os.remove(app.config['BASE_DIR'] + url_for('static',
                                                       filename='audio/' + song.mp3_filename))
        except:
            abort(500)
        # add delete from directory using song filename here
        db.session.delete(song)
        db.session.commit()
        db.session.close()
        return redirect(url_for('cms'))
    except:
        abort(500)


@app.route('/publish/<int:id>', methods=['POST'])
@login_required
def publish(id):
    try:
        # get song by  id
        song = Song.query.filter_by(id=id).first()
        # set published to true
        song.published = True
        # commit to database
        db.session.commit()
        db.session.close()
        return redirect(url_for('cms'))
    except:
        abort(500)


@app.route('/unpublish/<int:id>', methods=['POST'])
@login_required
def unpublish(id):
    try:
        # get song
        song = Song.query.filter_by(id=id).first()
        # set published to true
        song.published = False
        # commit to database
        db.session.commit()
        db.session.close()
        return redirect(url_for('cms'))
    except:
        abort(500)

# this currently uploads only to current directory fix that
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    try:
        if request.method == 'POST':
            # get name from the form & use secure_fileiname for
            # edgy and unifrom file name formatting
            name = secure_filename(request.form['name'])
            # get the mp3 & webm file & filenames and sanitize them
            webm_filename = secure_filename(audio.save(request.files['webm']))
            mp3_filename = secure_filename(audio.save(request.files['mp3']))
            # assign url to photo
            webm_url = audio.url(webm_filename)
            mp3_url = audio.url(mp3_filename)
            # create song object
            song = Song(name=name, webm_url=webm_url, webm_filename=webm_filename,
                        mp3_url=mp3_url, mp3_filename=mp3_filename)
            # insert song into database
            db.session.add(song)
            db.session.commit()
            db.session.close()
            return redirect(url_for('cms'))
        return render_template('upload.html')
    except:
        abort(500)

# ERROR HANDLING
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
