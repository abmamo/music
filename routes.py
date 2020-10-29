# flask
from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, current_app
# login 
from flask_login import login_required, login_user, logout_user
# db models
from models import Song, User
# app extensions
from app import ts, db, send_mail, audio
# secure filename
from werkzeug.utils import secure_filename
import os
# blueprint
player_bp = Blueprint("player_bp", __name__, url_prefix="/")


@player_bp.route('/', methods=['GET'])
def home():
    try:
        # get published songs
        songs = Song.query.filter_by(published=True).all()
        # render player
        return render_template('player.html', songs=songs)
    except:
        abort(500)

@player_bp.route('/about', methods=['GET'])
def about():
    try:
        return render_template('about.html')
    except:
        abort(500)

# AUTHENTICATION
@player_bp.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(400)

    try:
        # get the user using the email
        user = User.query.filter_by(email=email).first_or_404()
        # confirm user
        user.confirmed = True
        # save changes in database
        db.session.commit()
        db.session.close()
        # alert user
        flash("email confirmed")
        # redirect to sign in
        return redirect(url_for('signin'))
    except:
        abort(500)


@player_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            # get data from form
            email = request.form['email']
            password = request.form['password']
            # query by email
            user = User.query.filter_by(email=email).first()
            # check credentials
            if not user or not user.check_password(password):
                # alert user
                flash('invalid credentials')
                # redirect to sign in 
                return redirect(url_for('player_bp.signin'))
            # login user using the manager
            login_user(user)
            # redirect to upload page
            flash('signed in')
            # redirect to cms page
            return redirect(url_for('player_bp.cms'))
        # redner sign in page
        return render_template('signin.html')
    except:
        abort(500)


@player_bp.route('/reset', methods=['GET', 'POST'])
def reset():
    try:
        if request.method == 'POST':
            # get email from form
            email = request.form['email']
            # query user by emeail
            user = User.query.filter_by(email=email).first()
            # prepare email
            subject = "reset requested."
            # generate token
            token = ts.dumps(user.email, salt='recover-key')
            # build recover url
            recover_url = url_for(
                'player_bp.change',
                token=token,
                _external=True)
            # send the email
            send_mail(subject, current_app.config['MAIL_USERNAME'],
                      [email], recover_url)
            # alert user
            flash("reset link sent")
            # redirect to player
            return redirect(url_for('player_bp.home'))
        # render reset page
        return render_template('reset.html')
    except:
        abort(500)


@player_bp.route('/reset/<token>', methods=['GET', 'POST'])
def change(token):
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(400)
    # change password if valid token provided
    if request.method == 'POST':
        # get new password from form
        password = request.form['password']
        # get user using email
        user = User.query.filter_by(email=email).first_or_404()
        # set hashed password in database
        user.update_password(password)
        # save changes in database
        db.session.commit()
        db.session.close()
        # alert user
        flash("password changed")
        # redirect to sign in page
        return redirect(url_for('player_bp.signin'))
    # render password change page
    return render_template('change.html', token=token)

@player_bp.route('/signout')
def signout():
    try:
        # alert user
        flash('signed out')
        # sign out currently logged unser & redirect
        logout_user()
        # redirect to player
        return redirect(url_for('player_bp.home'))
    except:
        abort(500)


# CMS
@player_bp.route('/cms', methods=['GET'])
@login_required
def cms():
    try:
        # get all songs in the database
        songs = Song.query.order_by(Song.id.desc()).all()
        #print([song.mp3_filename for song in songs])
        return render_template('cms.html', songs=songs)
    except:
        abort(500)

@player_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        song = Song.query.filter_by(id=id).first()
        # try:
        # remove mp3 and webm files from disk if present
        webm_path = current_app.config['BASE_DIR'] + url_for('static',
                                                   filename='audio/' + song.webm_filename)
        mp3_path = current_app.config['BASE_DIR'] + url_for('static',
                                                   filename='audio/' + song.mp3_filename)
        # remove if they exist
        if os.path.exists(webm_path):
            # delete
            os.remove(webm_path)
        if os.path.exists(mp3_path):
            # delete
            os.remove(mp3_path)
        # delete from db
        db.session.delete(song)
        db.session.commit()
        db.session.close()
        # alert user
        flash('song deleted')
        # redirect to cms
        return redirect(url_for('player_bp.cms'))
    except:
        abort(500)


@player_bp.route('/publish/<int:id>', methods=['POST'])
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
        # alert user
        flash('published')
        # redirect to cms
        return redirect(url_for('player_bp.cms'))
    except:
        abort(500)


@player_bp.route('/unpublish/<int:id>', methods=['POST'])
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
        # alert user
        flash('unpublished')
        # redirect to cms
        return redirect(url_for('player_bp.cms'))
    except:
        abort(500)

@player_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    try:
        if request.method == 'POST':
            # get name from the form & use secure_fileiname for
            # edgy and unifrom file name formatting
            name = secure_filename(request.form['name'])
            # check if name already exists
            name_taken = Song.query.filter_by(name=name).first()
            # if found redirect back to upload
            if name_taken is not None:
                # alert user
                flash("name taken")
                # redirect
                return redirect(url_for("player_bp.upload"))
            # get files
            webm_file = request.files["webm"]
            mp3_file = request.files["mp3"]
            # get the mp3 & webm file & filenames and sanitize them
            webm_filename = secure_filename(name + ".webm")
            mp3_filename = secure_filename(name + ".mp3")
            # assign url to audio file
            webm_url = audio.url(webm_filename)
            mp3_url = audio.url(mp3_filename)
            # save audio files
            webm_file.save(os.path.join(current_app.config["UPLOADS_DEFAULT_DEST"], webm_filename))
            mp3_file.save(os.path.join(current_app.config["UPLOADS_DEFAULT_DEST"], mp3_filename))
            # create song object
            song = Song(name=name, webm_url=webm_url, webm_filename=webm_filename,
                        mp3_url=mp3_url, mp3_filename=mp3_filename)
            # insert song into database
            db.session.add(song)
            db.session.commit()
            db.session.close()
            # alert user
            flash('uploaded')
            # redirect to cms
            return redirect(url_for('player_bp.cms'))
        return render_template('upload.html')
    except:
        abort(500)