import pytest


def test_home_page(test_app):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get('/')
        assert response.status_code == 200