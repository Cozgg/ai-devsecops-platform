from django.conf import settings
from django.db import models

from common.models import ActiveTimeStampedModel


class Project(ActiveTimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "projects_project"
        indexes = [
            models.Index(fields=["owner", "active"]),
            models.Index(fields=["created_date"]),
        ]

    def __str__(self):
        return self.name
