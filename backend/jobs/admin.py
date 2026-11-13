from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "website",
                    "location", "created_at", "updated_at")
    list_select_related = ("owner",)
    search_fields = ("name", "owner__username", "location")
    list_filter = ("created_at", "updated_at")
