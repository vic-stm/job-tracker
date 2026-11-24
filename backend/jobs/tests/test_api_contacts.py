from django.urls import reverse

from jobs.models import Contact
from jobs.tests.factories import CompanyFactory


def test_cannot_create_contact_in_other_users_company(auth_client):
    other_company = CompanyFactory()
    payload = {"company": other_company.id, "name": "Hack"}

    response = auth_client.post(reverse("contact-list"), payload, format="json")

    assert response.status_code == 400
    assert "company" in response.json()
    assert not Contact.objects.filter(name="Hack").exists()
