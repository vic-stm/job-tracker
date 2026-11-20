from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from jobs.management.commands.seed_demo import DEMO_PASSWORD, DEMO_USERNAME
from jobs.models import Company, JobApplication, Note
from jobs.tests.factories import CompanyFactory, JobApplicationFactory


@pytest.fixture
def demo_user(db):
    call_command("seed_demo", stdout=StringIO())
    return get_user_model().objects.get(username=DEMO_USERNAME)


def test_seed_demo_creates_demo_user_with_known_password(demo_user):
    assert demo_user.check_password(DEMO_PASSWORD)


def test_seed_demo_is_idempotent(demo_user):
    companies_before = Company.objects.filter(owner=demo_user).count()
    applications_before = JobApplication.objects.filter(
        company__owner=demo_user).count()
    notes_before = Note.objects.filter(
        application__company__owner=demo_user).count()

    assert companies_before > 0

    call_command("seed_demo", stdout=StringIO())

    assert Company.objects.filter(owner=demo_user).count() == companies_before
    assert JobApplication.objects.filter(
        company__owner=demo_user).count() == applications_before
    assert Note.objects.filter(
        application__company__owner=demo_user).count() == notes_before


def test_seed_demo_restores_demo_password(demo_user):
    demo_user.set_password("new_password")
    demo_user.save()

    call_command("seed_demo", stdout=StringIO())

    demo_user.refresh_from_db()
    assert demo_user.check_password(DEMO_PASSWORD)


def test_reset_removes_data_created_by_visitors(demo_user):
    CompanyFactory(owner=demo_user, name="Garbage")

    call_command("seed_demo", reset=True, stdout=StringIO())

    assert not Company.objects.filter(owner=demo_user, name="Garbage").exists()


def test_reset_does_not_touch_other_users_data(demo_user):
    application = JobApplicationFactory()

    call_command("seed_demo", reset=True, stdout=StringIO())

    assert JobApplication.objects.filter(pk=application.pk).exists()
