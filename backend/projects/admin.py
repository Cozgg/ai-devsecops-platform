from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "active", "created_date", "updated_date")
    list_filter = ("active", "created_date")
    search_fields = ("name", "description", "owner__email", "owner__username")
    readonly_fields = ("created_date", "updated_date")
