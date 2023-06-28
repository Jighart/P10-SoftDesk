import pytest

from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework import status

client = APIClient()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db.json')


@pytest.fixture
def get_user1_token():
    response = client.post('/api/login/', data={
        'username': 'TestUser1',
        'password': 'SoftDesk1234'
    })
    token = response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == status.HTTP_200_OK
    return client


@pytest.fixture
def get_user2_token():
    response = client.post('/api/login/', data={
        'username': 'TestUser2',
        'password': 'SoftDesk1234'
    })
    token = response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == status.HTTP_200_OK
    return client


@pytest.mark.django_db
class TestProjects:

    def test_anonymous_user_gets_projects_list(self):
        response = APIClient().get('/api/projects/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_gets_projects_list(self, get_user1_token):
        response = get_user1_token.get('/api/projects/')
        assert response.status_code == status.HTTP_200_OK

    def test_user2_gets_project1_details(self, get_user2_token):
        response = get_user2_token.get('/api/projects/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_project(self, get_user1_token):
        errors = []
        project_data = {
            'title': 'Project 3',
            'description': 'Description of Project 3',
            'type': 'iOS'
        }
        response = get_user1_token.post('/api/projects/', project_data)

        if not response.status_code == status.HTTP_201_CREATED:
            errors.append("Wrong status code")
        if not response.json()['author'] == 1:
            errors.append("Wrong Author user ID")

        assert not errors

    def test_user_author_deletes_project1(self, get_user1_token):
        response = get_user1_token.delete('/api/projects/1/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_not_author_deletes_project1(self, get_user2_token):
        response = get_user2_token.delete('/api/projects/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_updates_project(self, get_user1_token):
        errors = []
        project_data = {
            'title': 'Project 1',
            'description': 'Description of Project 1',
            'type': 'iOS',
            'author': '2'
        }
        response = get_user1_token.put('/api/projects/1/', project_data)

        if not response.status_code == status.HTTP_200_OK:
            errors.append("Wrong status code")
        if not response.json()['author'] == 1:
            errors.append("Wrong Author user ID")

        assert not errors


@pytest.mark.django_db
class TestContributors:

    def test_user_gets_contributors_list(self, get_user1_token):
        response = get_user1_token.get('/api/projects/1/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_user_adds_new_contributor(self, get_user1_token):
        errors = []
        response = get_user1_token.post('/api/projects/1/users/', data={'user': '2', 'role': 'AUTHOR'})

        client = APIClient()
        login = client.post('/api/login/', data={
            'username': 'TestUser2',
            'password': 'SoftDesk1234'
        })
        token = login.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        new_contributor_can_access = client.get('/api/projects/1/')

        if not response.status_code == status.HTTP_201_CREATED:
            errors.append("Error during contributor creation")
        if not response.json()['role'] == 'CONTRIBUTOR':
            errors.append("Wrong role during contributor creation")
        if not new_contributor_can_access.status_code == status.HTTP_200_OK:
            errors.append("New contributor does not have access to the project")

        assert not errors

    def test_user_adds_non_existing_contributor(self, get_user1_token):
        response = get_user1_token.post('/api/projects/1/users/', data={'user': '1000'})
        assert response.json() == {'user': ['Invalid pk "1000" - object does not exist.']}

    def test_user_adds_duplicate_contributor(self, get_user2_token):
        response = get_user2_token.post('/api/projects/2/users/', data={'user': '1'})
        assert response.json() == {'non_field_errors': ['The fields project, user must make a unique set.']}

    @pytest.mark.parametrize('user, status_code',
                             [(444, status.HTTP_404_NOT_FOUND), (3, status.HTTP_204_NO_CONTENT),
                              (2, status.HTTP_406_NOT_ACCEPTABLE), (1, status.HTTP_400_BAD_REQUEST)])
    def test_author_deletes_contributor(self, get_user2_token, user, status_code):
        response = get_user2_token.delete(f'/api/projects/2/users/{user}')
        assert response.status_code == status_code


@pytest.mark.django_db
class TestIssues:

    def test_user_adds_issue_to_project(self, get_user1_token):
        issue_data = {
            'title': 'Test issue',
            'description': 'Description of this issue',
            'tag': 'TASK',
            'priority': 'MEDIUM',
            'status': 'IN PROGRESS'
        }

        response = get_user1_token.post('/api/projects/1/issues/', issue_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_updates_issue(self, get_user1_token):
        errors = []
        issue_data = {
            'title': 'New issue',
            'description': 'Description of this issue',
            'tag': 'TASK',
            'priority': 'MEDIUM',
            'status': 'IN PROGRESS'
        }
        response = get_user1_token.patch('/api/projects/1/issues/1', issue_data)

        if not response.status_code == status.HTTP_200_OK:
            errors.append("Wrong status code")
        if not response.json()['title'] == 'New issue':
            errors.append("Title not updated")

        assert not errors

    def test_user2_cannot_see_project1_issue(self, get_user2_token):
        response = get_user2_token.get('/api/projects/1/issues/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_see_project1_issue(self):
        response = APIClient().get('/api/projects/1/issues/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_deletes_his_issue(self, get_user1_token):
        response = get_user1_token.delete('/api/projects/1/issues/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestComments:

    def test_user_adds_comment_to_issue(self, get_user1_token):
        response = get_user1_token.post('/api/projects/1/issues/1/comments/', data={'description': 'Lorem ipsum dolor sit amet'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_updates_comment(self, get_user1_token):
        errors = []
        response = get_user1_token.patch('/api/projects/1/issues/1/comments/1', data={'description': 'Consectetur adipiscing elit'})

        if not response.status_code == status.HTTP_200_OK:
            errors.append("Wrong status code")
        if not response.json()['description'] == 'Consectetur adipiscing elit':
            errors.append("Description not updated")

        assert not errors

    def test_user_deletes_comment(self, get_user1_token):
        response = get_user1_token.delete('/api/projects/1/issues/1/comments/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user2_cannot_delete_user1_comment(self, get_user2_token):
        response = get_user2_token.delete('/api/projects/1/issues/1/comments/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_see_issue1_comments(self):
        response = APIClient().get('/api/projects/1/issues/1/comments/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
