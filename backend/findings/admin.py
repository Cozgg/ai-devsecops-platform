from django.contrib import admin

from findings.models import ScanFinding


@admin.register(ScanFinding)
class ScanFindingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "scan_job", "severity", "status", "scanner_name")
    list_filter = ("severity", "status", "scanner_name")
    search_fields = ("title", "description", "file_path", "scanner_name")
    readonly_fields = ("created_date", "updated_date")
