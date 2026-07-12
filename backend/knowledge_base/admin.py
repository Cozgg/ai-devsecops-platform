from django.contrib import admin

from knowledge_base.models import KnowledgeChunk, KnowledgeDocument


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "source_type", "category", "active", "created_date")
    list_filter = ("source_type", "category", "active")
    search_fields = ("title", "content", "source_url")
    readonly_fields = ("created_date", "updated_date")


@admin.register(KnowledgeChunk)
class KnowledgeChunkAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "chunk_index", "created_date")
    list_filter = ("created_date",)
    search_fields = ("document__title", "content")
    readonly_fields = ("created_date", "updated_date")
