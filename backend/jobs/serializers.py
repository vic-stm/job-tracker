from rest_framework import serializers

from .models import Company


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
