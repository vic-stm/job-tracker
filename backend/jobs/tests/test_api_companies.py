import pytest
from django.urls import reverse

from accounts.tests.factories import UserFactory
from jobs.models import Company
from jobs.tests.factories import CompanyFactory


def test_list_returns_only_own_companies(auth_client, user):
    own = CompanyFactory(owner=user)
    CompanyFactory()

    response = auth_client.get(reverse("company-list"))

    assert response.status_code == 200
    assert [c["id"] for c in response.json()] == [own.id]


def test_retrieve_other_users_company_returns_404(auth_client):
    other_company = CompanyFactory()

    response = auth_client.get(reverse("company-detail", args=[other_company.id]))

    assert response.status_code == 404


def test_create_sets_owner_to_current_user(auth_client, user):
    other_user = UserFactory()
    payload = {"name": "Acme", "owner": other_user.id}

    response = auth_client.post(reverse("company-list"), payload, format="json")

    assert response.status_code == 201
    company = Company.objects.get(pk=response.json()["id"])
    assert company.owner == user


def test_create_duplicate_name_returns_400(auth_client, user):
    CompanyFactory(owner=user, name="Acme")

    response = auth_client.post(
        reverse("company-list"), {"name": "Acme"}, format="json"
    )

    assert response.status_code == 400
    assert "name" in response.json()


@pytest.mark.django_db
def test_unauthenticated_request_is_rejected(api_client):
    response = api_client.get(reverse("company-list"))

    assert response.status_code == 403
