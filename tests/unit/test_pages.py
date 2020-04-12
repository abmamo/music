import pytest
from app import User


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_about_page(test_client):
    """
    Given a flask application test getting the about page
    """
    response = test_client.get('/about')
    assert response.status_code == 200


def test_signin_page(test_client):
    """
    Given a flask application test getting the signin page
    """
    response = test_client.get('/signin')
    assert response.status_code == 200


def test_signup_page(test_client):
    """
    Given a flask application test getting the signup page
    """
    response = test_client.get('/signup')
    assert response.status_code == 200


def test_reset_page(test_client):
    """
    Given a flask application test getting the reset page
    """
    response = test_client.get('/reset')
    assert response.status_code == 200


def test_cms_page(test_client):
    """
    Given a flask application test getting the cms page
    """
    response = test_client.get('/cms')
    assert response.status_code == 302


def test_upload_page(test_client):
    """
    Given a flask application test getting the upload page
    """
    response = test_client.get('/upload')
    assert response.status_code == 302
