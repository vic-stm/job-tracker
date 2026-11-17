from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from jobs.models import Company, Contact, JobApplication, Note, Technology

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"

APPLICATION_RELATED_KEYS = ("technologies", "notes")

DEMO_DATA = [
    {
        "company": {"name": "Acme Software", "website": "https://acme.example.com", "location": "Bilbao"},
        "contacts": [
            {"name": "Laura Pérez", "role": "Tech Recruiter",
                "email": "laura@acme.example.com"},
        ],
        "applications": [
            {
                "title": "Senior Angular Developer",
                "status": JobApplication.Status.INTERVIEWING,
                "work_mode": JobApplication.WorkMode.HYBRID,
                "seniority": JobApplication.Seniority.SENIOR,
                "salary_min": 45000,
                "salary_max": 55000,
                "location": "Bilbao",
                "technologies": ["Angular", "TypeScript", "RxJS"],
                "notes": ["First call with the recruiter went well.", "Technical interview next Tuesday."],
            },
            {
                "title": "Full Stack Developer (Angular + Django)",
                "status": JobApplication.Status.APPLIED,
                "work_mode": JobApplication.WorkMode.REMOTE,
                "seniority": JobApplication.Seniority.MID,
                "technologies": ["Angular", "Django", "PostgreSQL"],
                "notes": [],
            },
        ],
    },
    {
        "company": {"name": "Globex Labs", "website": "https://globex.example.com", "location": "Madrid"},
        "contacts": [
            {"name": "Mikel Etxeberria", "role": "Engineering Manager"},
        ],
        "applications": [
            {
                "title": "Backend Developer (Python)",
                "status": JobApplication.Status.TECHNICAL_TEST,
                "work_mode": JobApplication.WorkMode.REMOTE,
                "seniority": JobApplication.Seniority.MID,
                "salary_min": 40000,
                "salary_max": 48000,
                "technologies": ["Python", "Django", "Docker"],
                "notes": ["Take-home test: build a small REST API. Deadline Friday."],
            },
        ],
    },
    {
        "company": {"name": "Initech", "location": "Barcelona"},
        "contacts": [],
        "applications": [
            {
                "title": "Frontend Engineer",
                "status": JobApplication.Status.REJECTED,
                "work_mode": JobApplication.WorkMode.ON_SITE,
                "seniority": JobApplication.Seniority.SENIOR,
                "technologies": ["React", "TypeScript"],
                "notes": ["They were looking for more React experience."],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Create the demo user and sample data (idempotent). Use --reset to recreate it."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete the demo user's data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        user = self._get_or_create_demo_user()
        if options["reset"]:
            self._reset(user)
        for entry in DEMO_DATA:
            self._seed_company(user, entry)
        self.stdout.write(
            self.style.SUCCESS(f"Demo data ready for user '{DEMO_USERNAME}'"))

    def _get_or_create_demo_user(self):
        user, created = get_user_model().objects.get_or_create(username=DEMO_USERNAME)
        user.set_password(DEMO_PASSWORD)
        user.save()
        status = "Created" if created else "Found existing"
        self.stdout.write(f"{status} demo user '{DEMO_USERNAME}'")
        return user

    def _reset(self, user):
        deleted, _ = JobApplication.objects.filter(
            company__owner=user).delete()
        self.stdout.write(
            f"Deleted {deleted} applications and related objects")
        deleted, _ = Company.objects.filter(owner=user).delete()
        self.stdout.write(f"Deleted {deleted} companies and contacts")

    def _seed_company(self, user, entry):
        company_data = entry["company"]
        company, _ = Company.objects.get_or_create(
            owner=user,
            name=company_data["name"],
            defaults=company_data,
        )

        for contact_data in entry.get("contacts", []):
            Contact.objects.get_or_create(
                company=company,
                name=contact_data["name"],
                defaults=contact_data,
            )

        for app_data in entry.get("applications", []):
            self._seed_application(company, app_data)

    def _seed_application(self, company, app_data):
        fields = {k: v for k, v in app_data.items(
        ) if k not in APPLICATION_RELATED_KEYS}
        application, created = JobApplication.objects.get_or_create(
            company=company,
            title=app_data["title"],
            defaults=fields,
        )

        technologies = [
            Technology.objects.get_or_create(name=name)[0]
            for name in app_data.get("technologies", [])
        ]

        application.technologies.add(*technologies)

        if created:
            Note.objects.bulk_create(
                Note(application=application, body=body)
                for body in app_data.get("notes", [])
            )
