# tunez ![deploy](https://github.com/abmamo/tunez/workflows/deploy/badge.svg?branch=master)

A music player web application built using Flask + HowlerJS + SQLite. The appliciation is primarily divided into three parts: user facing music player, user authentication and authorization, and song management.  

## Quickstart

To successfully run this application there are 3 prerequisites:  python3, a valid gmail address to send account confirmation and recovery emails which is stored locally, and the dependencies listed in the requirements.txt file. To run the application:

- clone repo
   ```
   git clone git@github.com:abmamo/music.git
   ```
- create virtual env
   ```
   cd tunez &&
   python3 -m venv env
   ```
- activate virtual env
   ```
   source env/bin/activate
   ```
- install dependencies
   ```
   pip install -r requirements.txt
   ```
- create and store configuration in .env (sample stored in .env.sample)
   ```
   DOMAIN = if running locally "http://127.0.0.1:5000" otherwise actual domain
   ENVIRONMENT = "development" # environment
   SERVER_NAME = "127.0.0.1:5000" # same as domain 
   MAIL_SERVER = "mail server for e.g. smtp.google.com"
   MAIL_USERNAME = "mail address"
   MAIL_PASSWORD = "mail password"
   USER_EMAIL = "sign in email here"
   USER_PASSWORD = "sign in password here"
   ```
6. run
   ```
   python wsgi.py
   ```
