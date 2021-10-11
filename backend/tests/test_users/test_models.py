import pytest


@pytest.mark.django_db(transaction=True)
def test_users_not_auth(client):
    response = client.get('/api/users/')
    assert response.status_code == 200, (
        'Страница недоступна!'
    )

def test_admin_user(admin):
    assert admin.username == 'TestAdmin'
