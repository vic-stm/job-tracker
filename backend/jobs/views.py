from rest_framework import viewsets

from .models import Company, Contact, JobApplication, Note
from .serializers import (
    CompanySerializer,
    ContactSerializer,
    JobApplicationSerializer,
    NoteSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        return (
            JobApplication.objects.filter(company__owner=self.request.user)
            .select_related("company")
            .prefetch_related("technologies")
        )


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(application__company__owner=self.request.user)
        application_id = self.request.query_params.get("application")
        if application_id is not None:
            queryset = queryset.filter(application_id=application_id)
        return queryset


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.filter(company__owner=self.request.user)
        company_id = self.request.query_params.get("company")
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset
