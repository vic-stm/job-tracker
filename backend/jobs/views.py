from rest_framework import viewsets

from .models import Company, JobApplication
from .serializers import CompanySerializer, JobApplicationSerializer


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
