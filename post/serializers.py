from rest_framework import serializers

from .models import Post
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "bus_name",
            "is_vendor",
            "is_verified",
            "profile_image",
        ]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

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
