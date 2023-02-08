from rest_framework import serializers

from .models import Post
from user.serializers import UserInfoSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "category",
            "name",
            "description",
            "price",
            "condition",
            "image1",
            "image2",
            "image3",
            "is_sold",
            "likes",
            "comments",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "comments", "likes"]
