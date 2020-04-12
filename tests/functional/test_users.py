import pytest
from app import User, db


@pytest.fixture(scope='module')
def new_user():
    user = User('test@test.com', 'testpassword')
    return user


def test_new_user_sign_up(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, confirmed, and role fields are defined correctly
    """
    assert new_user.email == 'test@test.com'
    assert new_user.password != 'testpassword'
    assert not new_user.confirmed


def test_new_user_sign_in_sign_out(test_client, new_user):
    """
    Given a User model sign it in and see if you get a 302 to a 200 redirect
    """
    response = test_client.post('/signin',
                                data=dict(email=new_user.email,
                                          password=new_user.password),
                                follow_redirects=True)

    assert response.status_code == 200
    response = test_client.get('/signout', follow_redirects=True)
    assert response.status_code == 200
