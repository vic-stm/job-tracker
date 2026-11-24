import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.tests.factories import UserFactory


def test_login_with_valid_credentials_starts_session(api_client, user):
    payload = {"username": user.username, "password": "password123"}

    login_response = api_client.post(reverse("auth-login"), payload, format="json")
    me_response = api_client.get(reverse("auth-me"))

    assert login_response.status_code == 200
    assert me_response.status_code == 200
    assert me_response.json()["username"] == user.username


def test_login_with_wrong_password_returns_400(api_client, user):
    payload = {"username": user.username, "password": "wrong-secret"}

    login_response = api_client.post(reverse("auth-login"), payload, format="json")
    me_response = api_client.get(reverse("auth-me"))

    assert login_response.status_code == 400
    assert me_response.status_code == 403


@pytest.mark.django_db
def test_me_requires_authentication(api_client):
    response = api_client.get(reverse("auth-me"))

    assert response.status_code == 403


def test_logout_ends_session(api_client, user):
    api_client.login(username=user.username, password="password123")

    logout_response = api_client.post(reverse("auth-logout"))
    me_response = api_client.get(reverse("auth-me"))

    assert logout_response.status_code == 204
    assert me_response.status_code == 403


@pytest.mark.django_db
def test_login_requires_csrf_token():
    client = APIClient(enforce_csrf_checks=True)
    user = UserFactory()
    payload = {"username": user.username, "password": "password123"}

    response = client.post(reverse("auth-login"), payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_login_succeeds_with_csrf_token():
    client = APIClient(enforce_csrf_checks=True)
    user = UserFactory()
    client.get(reverse("auth-csrf"))
    token = client.cookies["csrftoken"].value

    response = client.post(
        reverse("auth-login"),
        {"username": user.username, "password": "password123"},
        format="json",
        HTTP_X_CSRFTOKEN=token,
    )

    assert response.status_code == 200


def test_login_is_throttled_after_five_attempts(api_client, user):
    payload = {"username": user.username, "password": "wrong-secret"}
    for _ in range(5):
        api_client.post(reverse("auth-login"), payload, format="json")

    response = api_client.post(reverse("auth-login"), payload, format="json")
    assert response.status_code == 429


def test_failed_login_is_logged_without_password(api_client, user, caplog):
    payload = {"username": user.username, "password": "wrong-secret"}

    api_client.post(reverse("auth-login"), payload, format="json")

    assert "Failed login" in caplog.text
    assert user.username in caplog.text
    assert "wrong-secret" not in caplog.text
