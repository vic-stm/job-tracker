from rest_framework import serializers

from .models import Company, JobApplication, Note, Technology


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "website",
            "location",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        user = self.context["request"].user
        companies = Company.objects.filter(owner=user, name=value)
        if self.instance:
            companies = companies.exclude(pk=self.instance.pk)
        if companies.exists():
            raise serializers.ValidationError(
                "You already have a company with this name."
            )
        return value


class JobApplicationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    technologies = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Technology.objects.all(), required=False
    )

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "company",
            "company_name",
            "title",
            "url",
            "raw_description",
            "technologies",
            "salary_min",
            "salary_max",
            "currency",
            "work_mode",
            "seniority",
            "location",
            "status",
            "applied_on",
            "next_action",
            "next_action_on",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request is not None:
            self.fields["company"].queryset = Company.objects.filter(owner=request.user)

    def validate(self, attrs):
        salary_min = attrs.get("salary_min", getattr(self.instance, "salary_min", None))
        salary_max = attrs.get("salary_max", getattr(self.instance, "salary_max", None))
        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise serializers.ValidationError(
                {
                    "salary_max": "Maximum salary must be greater than or equal to minimum salary."
                }
            )
        return attrs


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "application", "body", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request is not None:
            self.fields["application"].queryset = JobApplication.objects.filter(
                company__owner=request.user
            )
