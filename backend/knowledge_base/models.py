from django.db import models

from common.models import ActiveTimeStampedModel, TimeStampedModel


class KnowledgeDocument(ActiveTimeStampedModel):
    class SourceType(models.TextChoices):
        OWASP = "OWASP", "OWASP"
        CWE = "CWE", "CWE"
        SEMGREP_DOC = "SEMGREP_DOC", "Semgrep Doc"
        TRIVY_DOC = "TRIVY_DOC", "Trivy Doc"
        CUSTOM_NOTE = "CUSTOM_NOTE", "Custom Note"
        RUNBOOK = "RUNBOOK", "Runbook"

    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50, choices=SourceType.choices)
    category = models.CharField(max_length=100, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    content = models.TextField()

    class Meta:
        db_table = "knowledge_base_document"
        indexes = [
            models.Index(fields=["source_type", "active"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title


class KnowledgeChunk(TimeStampedModel):
    document = models.ForeignKey(
        KnowledgeDocument,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    chunk_index = models.IntegerField()
    content = models.TextField()
    embedding_json = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "knowledge_base_chunk"
        indexes = [
            models.Index(fields=["document", "chunk_index"]),
            models.Index(fields=["created_date"]),
        ]

    def __str__(self):
        return f"{self.document.title} - chunk {self.chunk_index}"
