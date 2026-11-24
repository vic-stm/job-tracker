from django.urls import reverse

from jobs.models import JobApplication
from jobs.tests.factories import (
    CompanyFactory,
    JobApplicationFactory,
    TechnologyFactory,
)


def test_cannot_create_application_in_other_users_company(auth_client):
    other_company = CompanyFactory()
    payload = {"company": other_company.id, "title": "Hack"}

    response = auth_client.post(reverse("application-list"), payload, format="json")

    assert response.status_code == 400
    assert "company" in response.json()
    assert not JobApplication.objects.filter(title="Hack").exists()


def test_salary_min_greater_than_max_returns_400(auth_client, user):
    company = CompanyFactory(owner=user)
    payload = {
        "company": company.id,
        "title": "Backend developer",
        "salary_min": 50000,
        "salary_max": 40000,
    }

    response = auth_client.post(reverse("application-list"), payload, format="json")

    assert response.status_code == 400
    assert "salary_max" in response.json()


def test_patch_salary_min_is_validated_against_stored_max(auth_client, user):
    application = JobApplicationFactory(company__owner=user, salary_max=40000)

    response = auth_client.patch(
        reverse("application-detail", args=[application.id]),
        {"salary_min": 50000},
        format="json",
    )

    assert response.status_code == 400
    assert "salary_max" in response.json()


def test_list_has_no_n_plus_one(auth_client, user, django_assert_num_queries):
    company = CompanyFactory(owner=user)
    technology = TechnologyFactory()

    for application in JobApplicationFactory.create_batch(3, company=company):
        application.technologies.add(technology)

    with django_assert_num_queries(2):
        response = auth_client.get(reverse("application-list"))

    assert response.status_code == 200
    assert len(response.json()) == 3
