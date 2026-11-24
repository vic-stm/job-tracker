from django.urls import reverse

from jobs.models import Note
from jobs.tests.factories import JobApplicationFactory


def test_cannot_create_notes_in_other_users_application(auth_client):
    other_application = JobApplicationFactory()
    payload = {"application": other_application.id, "body": "Hack"}

    response = auth_client.post(reverse("note-list"), payload, format="json")

    assert response.status_code == 400
    assert "application" in response.json()
    assert not Note.objects.filter(body="Hack").exists()
