import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'username': 'TestUser1',
        'email': 'testuser1@example.com',
        'first_name': 'Test',
        'last_name': 'User1',
        'password': 'testpassword',
        'password2': 'testpassword'
    }


@pytest.fixture
def user_data2():
    return {
        'username': 'TestUser2',
        'email': 'testuser2@example.com',
        'first_name': 'Test',
        'last_name': 'User2',
        'password': 'testpassword',
        'password2': 'testpassword'
    }


@pytest.fixture
def project_data():
    return {
        'title': 'Project 1',
        'description': 'Description of Project 1',
        'type': 'BACKEND'
    }


@pytest.fixture
def project_data2():
    return {
        'title': 'Project 2',
        'description': 'Description of Project 2',
        'type': 'FRONTEND'
    }


@pytest.fixture
def get_user1_token(api_client, user_data):
    api_client.post('/api/signup/', data=user_data)
    response = api_client.post('/api/login/', data={
        'username': user_data['username'],
        'password': user_data['password']
    })
    token = response.json()['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == status.HTTP_200_OK
    return api_client


@pytest.fixture
def get_user2_token(api_client, user_data2):
    api_client.post('/api/signup/', data=user_data2)
    response = api_client.post('/api/login/', data={
        'username': user_data2['username'],
        'password': user_data2['password']
    })
    token = response.json()['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == status.HTTP_200_OK
    return api_client


@pytest.fixture
def create_project1(get_user1_token, project_data):
    response = get_user1_token.post('/api/projects/', project_data)
    assert response.status_code == status.HTTP_201_CREATED
    return get_user1_token


@pytest.fixture
def create_project2(get_user2_token, project_data2):
    response = get_user2_token.post('/api/projects/', project_data2)
    assert response.status_code == status.HTTP_201_CREATED
    return get_user2_token


@pytest.mark.django_db
def test_anonymous_user_gets_projects_list(api_client):
    response = api_client.get('/api/projects/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user2_gets_project1_details(create_project1, get_user2_token):
    response = get_user2_token.get('/api/projects/1/')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_gets_projects_list(create_project1, get_user1_token):
    response = get_user1_token.get('/api/projects/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_deletes_project1(create_project1):
    response = create_project1.delete('/api/projects/1/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

@pytest.mark.django_db
def test_user_gets_contributors_list(create_project1, get_user1_token):
    response = get_user1_token.get('/api/projects/1/users/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_adds_new_contributor(create_project1, user_data2):
    create_project1.post('/api/signup/', user_data2)
    response = create_project1.post('/api/projects/1/users/', data={'user': '2'})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_new_contributor_can_access_project(create_project1, user_data2):
    create_project1.post('/api/signup/', user_data2)
    create_project1.post('/api/projects/1/users/', data={'user': '2'})
    
    client = APIClient()
    login = client.post('/api/login/', data={
        'username': user_data2['username'],
        'password': user_data2['password']
    })
    token = login.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/projects/1/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_adds_new_author(create_project1, user_data2):
    create_project1.post('/api/signup/', user_data2)
    response = create_project1.post('/api/projects/1/users/', data={'user': '2', 'role': 'AUTHOR'})
    assert response.json()['role'] == 'CONTRIBUTOR'


@pytest.mark.django_db
def test_user_adds_non_existing_contributor(create_project1):
    response = create_project1.post('/api/projects/1/users/', data={'user': '100'})
    assert response.json() == {'user': ['Invalid pk "100" - object does not exist.']}


@pytest.mark.django_db
def test_user_adds_duplicate_contributor(create_project1):
    response = create_project1.post('/api/projects/1/users/', data={'user': '1'})
    assert response.json() == {'non_field_errors': ['The fields project, user must make a unique set.']}


