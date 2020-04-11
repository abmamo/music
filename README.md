# music

As a developer it is easy to fall/be put in a box of someone who spends their majority of time writing abstract code. I am passionate about pushing the boundaries of development and exploring activities, hobbies, and projects that combine coding and other disciplines. This is a music player web application built using Flask + HowlerJS + SQLite. It is a music player with a content management system for uploading and removing songs.

## Quickstart

The application was built using Flask and needs python installed to work. To run the application:

1. Create a virtual environment
   ```
   python3 -m venv env
   ```
2. Install all the requirements listed in the requirements file
   ```
   pip install -r requirements.txt
   ```
3. Run the application. It will open in your browser at 127.0.0.1
   ```
   python wsgi.py
   ```
4. Head over to http://localhost:5000/signup to create an account
5. Once you sign up a confirmation email will be sent to the email account used for signup. Once you confirm your account you will be redirected to the signin page.
6. Once you sign in if you head over to http://localhost:5000/upload you fill be presented with a form with 3 fields: the song name field, the mp3 file upload field, and the webm file upload field.
7. After the upload completes the application will redirect you to http://localhost:5000/cms where you can publish, unpublish, or delete the song. Only after a song is published is it accessible by the music player.


## Technical Overview:

The web server is built using Flask. It is roughly divided into three components: the music player, the song management dashboard, and auth components. 

The music player is built using HowlerJS, vanilla JavaScript and CSS. It has volume control, seeking, next/previous and all the things you want in a music player implemented. It needs both .webm and .mp3 files to be able to function. It is built in JavaScript and CSS.

The song management dashboard and auth components on the other hand are built using HTML/CSS on the frontend and SQLite + SQLAlchemy + Flask for the backend. The user uploads a given song which is saved in a database. The database keeps a record of the song ID, the song Name, the song mp3 and webm files and a boolean field published to check if a given song has been published. The name of the song in addition to the location of the audio files on disk is saved in the database. The javascript music player is then passed a list of song SQLAlchemy objects from which it gets the audio files and the song names. Due to variety of filenames that can be uploaded to servers they are currently sanitized using secure_filename. 

When a person publishes a song it modifies the published field of the song object and makes it visible to the music player. If a person deletes a song first the files associated with that song are deleted and then the entry for that song in the database itself deleted.
