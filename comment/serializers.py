from rest_framework import serializers

from .models import Comment


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

    class Meta:
        model = Comment
        fields = "__all__"
