from django.db import models
from django.conf import settings
from django.utils.text import Truncator


class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "companies"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="unique_company_name_per_owner"),
        ]

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "technologies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class JobApplication(models.Model):
    class WorkMode(models.TextChoices):
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        ON_SITE = "on_site", "On Site"

    class Seniority(models.TextChoices):
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"
        LEAD = "lead", "Lead"

    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEWING = "interviewing", "Interviewing"
        TECHNICAL_TEST = "technical_test", "Technical Test"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    company = models.ForeignKey(
        Company,
        related_name="applications",
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    raw_description = models.TextField(blank=True)
    technologies = models.ManyToManyField(
        Technology, related_name="applications", blank=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, default="EUR")
    work_mode = models.CharField(max_length=20, choices=WorkMode, blank=True)
    seniority = models.CharField(max_length=20, choices=Seniority, blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20, choices=Status, default=Status.SAVED)
    applied_on = models.DateField(null=True, blank=True)
    next_action = models.CharField(max_length=200, blank=True)
    next_action_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(salary_min__lte=models.F('salary_max')),
                name='jobapplication_salary_min_lte_max',
                violation_error_message="Minimum salary cannot be greater than maximum salary.",
            )
        ]

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Contact(models.Model):
    company = models.ForeignKey(
        Company,
        related_name="contacts",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Note(models.Model):
    application = models.ForeignKey(
        JobApplication,
        related_name="notes",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return Truncator(self.body).chars(50)
