from rest_framework import serializers
from projects.models import Project,ProjectTag
from users.serializers import UserSerializer
from users.models import User

class ProjectTagSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectTag
        fields = ["id", "project", "user", "role"]




class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    members = ProjectTagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "members",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        owner_id = self.context["request"].user.id
        validated_data["owner_id"] = owner_id
        return super().create(validated_data)