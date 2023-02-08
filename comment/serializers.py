from rest_framework import serializers

from .models import Comment
from user.serializers import UserInfoSerializer


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "created_at", "body"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class GetCommentSerializer(serializers.ModelSerializer):
    replies = CommentSerializer(many=True)
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Comment
        fields = "__all__"
