from django.contrib import admin

from ai_agents.models import AIReport


@admin.register(AIReport)
class AIReportAdmin(admin.ModelAdmin):
    list_display = ("id", "scan_job", "model_name", "created_date")
    list_filter = ("model_name", "created_date")
    search_fields = ("summary", "risk_overview", "recommendation", "model_name")
    readonly_fields = ("created_date", "updated_date")
