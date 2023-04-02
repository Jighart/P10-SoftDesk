import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def credentials():
    credentials = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'TestUser',
        'email': 'testuser@testing.com',
        'password': 'TestPassword',
        'password2': 'TestPassword'
    }
    return credentials


@pytest.mark.django_db
def test_create_user(client, credentials):
    response = client.post('/api/signup/', credentials)
    assert response.status_code == 201

@pytest.mark.django_db
def test_login(client, credentials):
    client.post('/api/signup/', credentials)
    response = client.post('/api/login/', {'username': 'TestUser', 'password': 'TestPassword'})
    assert response.status_code == 200