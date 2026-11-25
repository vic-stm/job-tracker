import django_filters

from .models import JobApplication


class JobApplicationFilter(django_filters.FilterSet):
    technology = django_filters.CharFilter(
        field_name="technologies__name", lookup_expr="iexact"
    )

    class Meta:
        model = JobApplication
        fields = ["work_mode", "status"]
