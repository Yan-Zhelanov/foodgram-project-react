from pytest import fixture


@fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
         email='test-admin@gmail.com', username='TestAdmin', password='admin'
    )


@fixture
def token(admin):
    from rest_framework.authtoken.models import Token
    Token.objects.create(user=admin)
    return {'auth_token': token.key}


@fixture
def user_client(token):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token["auth_token"]}')
    return client
