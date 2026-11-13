from django.contrib import admin

from .models import Company, Technology, JobApplication


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "website",
                    "location", "created_at", "updated_at")
    list_select_related = ("owner",)
    search_fields = ("name", "owner__username", "location")
    list_filter = ("created_at", "updated_at")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("company", "title", "work_mode", "seniority",
                    "status", "applied_on", "created_at", "updated_at")
    list_select_related = ("company",)
    search_fields = ("title", "company__name")
    list_filter = ("work_mode", "seniority", "status",
                   "applied_on", "created_at", "updated_at")
    filter_horizontal = ("technologies",)
