import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def credentials():
    return {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'TestUser',
        'email': 'testuser@testing.com',
        'password': 'TestPassword',
        'password2': 'TestPassword'
    }


@pytest.mark.django_db
def test_create_user(client, credentials):
    response = client.post('/api/signup/', credentials)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_login(client, credentials):
    client.post('/api/signup/', credentials)
    response = client.post('/api/login/', {'username': 'TestUser', 'password': 'TestPassword'})
    assert response.status_code == status.HTTP_200_OK