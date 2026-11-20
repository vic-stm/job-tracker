import factory

from accounts.tests.factories import UserFactory
from jobs.models import Company, Contact, JobApplication, Note, Technology


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Company {n}")


class TechnologyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Technology

    name = factory.Sequence(lambda n: f"Technology {n}")


class JobApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobApplication

    company = factory.SubFactory(CompanyFactory)
    title = factory.Faker("job")


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    company = factory.SubFactory(CompanyFactory)
    name = factory.Faker("name")


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    application = factory.SubFactory(JobApplicationFactory)
    body = factory.Faker("sentence")
