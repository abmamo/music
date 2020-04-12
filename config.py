# Statement for enabling the development environment
import os
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'music.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = False
WTF_CSRF_ENABLED = False

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Uploads
#UPLOADS_DEFAULT_DEST = BASE_DIR + 'app/static/images/'
UPLOADS_DEFAULT_DEST = "./app/static/images/"
UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/images/'

#UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, '/app/static/images/')
UPLOADS_IMAGES_DEST = "./app/static/images/"
UPLOADED_IMAGES_URL = 'http://localhost:5000/static/images/'

# email configuration
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'YOUR GMAIL EMAIL ADDRESS HERE'
MAIL_PASSWORD = 'YOUR GMAIL PASSWORD HERE'
# set max users
MAX_USERS_NOT_REACHED = True
