from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "owner",
            "name",
            "description",
            "active",
            "created_date",
            "updated_date",
        )
        read_only_fields = ("id", "owner", "active", "created_date", "updated_date")
