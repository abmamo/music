# music
Case Study:

As a computer science major and developer it is easy to fall in a box. And as a developer who has spent the majority of the past 5 years typing away in VSCode I am passionate about exploring activities and hobbies beyond coding. This has led me to pursue and participate in projects that are an intersection between coding and other disciples such as art and music. 

This web application is a web music player built using Flask + HowlerJS + SQLite. It is a music player with a content management system for uploading and removing songs and creating playlists. 


Technical Overview:

The web server is built using Flask. It is roughly divided into three components: the music player, the song management dashboard, and auth components. 

The music player is built using HowlerJS, vanilla JavaScript and CSS. It has volume control, seeking, next/previous and all the things you want in a music player implemented. It needs both .webm and .mp3 files to be able to function. 

The song management dashboard and auth components on the other hand are built using HTML/CSS on the frontend and SQLite + SQLAlchemy + Flask for the backend

How it works:

The application is divided into two main parts. The user facing music player built in javascript and css and the song management cms built using SQLite/SQLAclhemy and Flask. The user uploads a given song which is saved in a database. The database keeps a record of the song ID, the song Name, the song mp3 and webm files and a boolean field published to check if a given song has been published. When a user uploads a song the name of the song in addition to the disk location of the audio files is saved in the database. The javascript music player is then passed a list of song SQLAlchemy objects from which it gets the audio file and the song names. Due to variety of filenames that can be uploaded to servers they are sanitized using secure_filename. 

When a person publishes a song it modifies the published field of the song object and makes it visible to the music player. If a person deletes a song first the files associated with that song are deleted and then the entry for that song in the database itself deleted.

Challenges:
Uploading song files which have variable sizes proved to be a challenge. I got around this by changing the client max body size parameter in the nginx configuration file.
