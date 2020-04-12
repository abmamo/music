# music

A music player web application built using Flask + HowlerJS + SQLite. The appliciation is primarily divided into three parts: user facing music player, user authentication and authorization, and song management.  

## Quickstart

To successfully run this application there are 3 prerequisites:  python3, a valid gmail address to send account confirmation and recovery emails which is stored locally, and the dependencies listed in the requirements.txt file. To run the application:

1. Clone the repo
   ```
   git clone git@github.com:abmamo/music.git
   ```
2. Navigate into the directory and create a python virtual environment
   ```
   cd music &&
   python3 -m venv env
   ```
3. Activate the virtual environment
   ```
   source env/bin/activate
   ```
4. Install all the dependencies listed in the requirements file
   ```
   pip install -r requirements.txt
   ```
5. Configure mail settings to be able to utilize account confirmation and password reset services by setting
   ```
   MAIL_USERNAME = 'YOUR GMAIL EMAIL ADDRESS HERE'
   MAIL_PASSWORD = 'YOUR GMAIL PASSWORD HERE'
   ```
6. Run the application. It will open in your browser at 127.0.0.1
   ```
   python wsgi.py
   ```
7. Head over to http://localhost:5000/signup to create an account. An email will be sent to your account to activate your account.
8. Once you sign up a confirmation email will be sent to the email account used for signup. Once you confirm your account you will be redirected to the signin page.
9. Once you sign in if you head over to http://localhost:5000/upload you fill be presented with a form with 3 fields: the song name field, the mp3 file upload field, and the webm file upload field.
10. After the upload completes the application will redirect you to http://localhost:5000/cms where you can publish, unpublish, or delete the song. Only after a song is published is it accessible by the music player.

## Technical Overview

The music player is built using HowlerJS, vanilla JavaScript and CSS. It has volume control, seeking, next/previous and all the things you want in a music player implemented. It needs both .webm and .mp3 files to be able to function. It is built in JavaScript and CSS.

The web server is built using Flask and is divided into three components. The views serving the music player, the song management, and user handling. Since the music player is primarily built using HowlerJS and CSS it only needs the server to get a published list of songs and the rest of the work is handled on the front end. The user handling routes allow users to signup, signin, signout, reset password, and confirm their email accounts while the song management routes handle song upload, publication, and deletion. The server does this by utilizing SQLAlchemy to store information in a locally stored SQLite database.

There are two SQLAlchemy classes for interfacing with the database: the user class and the song class. The user class has the fields id, email, password and confirmed while the song class has id, name, webm_filename, mp3_filename, webm_url, and published.

When a user signs up, they are assigned a unique id and their email and password is stored in the database and the confirmed field set to False. Once they confirm their email account the confirmed field will be set to True. Similarly, when a user uploads a song the .webm and .mp3 files are saved to disk and their filenames and location on disk in addition to the name of the song are stored in the database. By default all uploaded songs have the published field set to False.


