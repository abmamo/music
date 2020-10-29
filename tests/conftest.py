import os
import pytest

@pytest.fixture(scope='module')
def test_app():
    from app import app as test_app
    yield test_app
    # if test db exists delete
    if os.path.exists(os.path.join(test_app.config["BASE_DIR"], "teret.test.db")):
        # get base dir
        os.remove(os.path.join(test_app.config["BASE_DIR"], "teret.test.db"))



@pytest.fixture(scope="module")
def test_db(test_app):
    # with app context
    with test_app.app_context():
        # import db extension
        from app.extensions import db as test_db
        # create database tables
        test_db.create_all()
        # yield session
        yield test_db
        # drop all tables created
        test_db.drop_all()