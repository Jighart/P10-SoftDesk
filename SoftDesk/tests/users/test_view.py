import pytest
from django.test import Client


@pytest.fixture
def api_client():
    return Client()

@pytest.mark.django_db
def test_create_user(api_client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpassword',
        'password2': 'testpassword',
    }
    response = api_client.post('/api/signup/', user_data)
    assert response.status_code == 201