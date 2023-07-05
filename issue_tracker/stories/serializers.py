from rest_framework import serializers
from stories.models import Story





class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Story
        fields= [
            "id",
            "title",
            "description",
            "assignee",
            "estimated_time",
            "project",
            "status",
            "is_scheduled",
            "created_at",
            "updated_at",
        ]
        ordering = [
            "-status",
            "created_at",
        ]