from django.contrib import admin

from scans.models import ScanJob


@admin.register(ScanJob)
class ScanJobAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "created_by", "status", "scan_type", "created_date")
    list_filter = ("status", "scan_type", "created_date")
    search_fields = ("project__name", "created_by__email", "created_by__username")
    readonly_fields = ("created_date", "updated_date", "started_at", "finished_at")
