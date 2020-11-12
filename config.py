from dotenv import load_dotenv
# Statement for enabling the development environment
import os
# load env
load_dotenv()

class Config:
    # blog name
    APP_NAME = "yared.io"
    # app dir
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # application threads. a common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.urandom(64)
    # Secret key for signing cookies
    SECRET_KEY = os.urandom(64)
    # Uploads
    # UPLOADS_DEFAULT_DEST = BASE_DIR + 'app/static/audio/'
    UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, "static/audio/")
    UPLOADS_DEFAULT_URL = os.environ.get("DOMAIN") + "/static/"
    # UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, '/app/static/images/')
    UPLOADS_AUDIO_DEST = os.path.join(BASE_DIR, "static/audio/")
    UPLOADED_AUDIO_URL = os.environ.get("DOMAIN") + "/static/"
    # email configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # server name
    SERVER_NAME = os.environ.get("SERVER_NAME")
    SESSION_COOKIE_DOMAIN = os.environ.get("SERVER_NAME")
    DOMAIN = os.environ.get("DOMAIN")

class TestingConfig(Config):
    # db 
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "music.test.db")
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    # set admin
    USER_EMAIL = "test@test.com"
    USER_PASSWORD = "testpassword"

class DevelopmentConfig(Config):
    # db 
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "music.dev.db")
    DEBUG = True
    TESTING = True
    # set admin
    USER_EMAIL = os.environ.get("USER_EMAIL")
    USER_PASSWORD = os.environ.get("USER_PASSWORD")


class ProductionConfig(Config):
    # db
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "music.db")
    DEBUG = False
    # set admin
    USER_EMAIL = os.environ.get("USER_EMAIL")
    USER_PASSWORD = os.environ.get("USER_PASSWORD")
