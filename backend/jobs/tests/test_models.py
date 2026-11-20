import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError

from jobs.models import Company, JobApplication, Note
from jobs.tests.factories import (
    CompanyFactory,
    JobApplicationFactory,
    NoteFactory,
    TechnologyFactory,
)


@pytest.mark.django_db
def test_technology_str_returns_name():
    technology = TechnologyFactory(name="Django")

    assert str(technology) == "Django"


@pytest.mark.django_db
def test_company_name_is_unique_per_owner():
    company = CompanyFactory(name="Acme")

    with pytest.raises(IntegrityError):
        CompanyFactory(name="Acme", owner=company.owner)


@pytest.mark.django_db
def test_different_owners_can_have_same_company_name():
    CompanyFactory(name="Acme")
    CompanyFactory(name="Acme")

    assert Company.objects.filter(name="Acme").count() == 2


@pytest.mark.django_db
def test_salary_min_cannot_be_greater_than_max():
    with pytest.raises(IntegrityError):
        JobApplicationFactory(salary_min=50000, salary_max=40000)


@pytest.mark.django_db
def test_salary_range_can_be_partial():
    JobApplicationFactory(salary_min=50000, salary_max=None)

    assert JobApplication.objects.filter(
        salary_min=50000, salary_max__isnull=True
    ).exists()


@pytest.mark.django_db
def test_company_with_applications_cannot_be_deleted():
    company = CompanyFactory()
    JobApplicationFactory(company=company)

    with pytest.raises(ProtectedError):
        company.delete()


@pytest.mark.django_db
def test_deleting_application_deletes_its_notes():
    note = NoteFactory()

    note.application.delete()

    assert not Note.objects.filter(pk=note.pk).exists()
