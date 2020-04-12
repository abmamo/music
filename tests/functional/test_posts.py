import pytest
from app import User, db


@pytest.fixture(scope='module')
def new_user():
    user = User('test@test.com', 'testpassword')
    return user


def test_cms_access_with_login(new_user, test_client):
    """
    Given a user model try to access the cms after signing in
    """
    # signin user
    response = test_client.post('/signin',
                                data=dict(email=new_user.email,
                                          password=new_user.password),
                                follow_redirects=True)
    # request acess to cms
    response = test_client.get('/cms', follow_redirects=True)
    assert response.status_code == 200
