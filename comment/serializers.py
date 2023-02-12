from rest_framework import serializers

from .models import Comment
from user.models import User
from user.serializers import UserInfoSerializer


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "created_at", "body"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Comment
        fields = "__all__"


class GetCommentSerializer(serializers.ModelSerializer):
    # replies = CommentSerializer(many=True)
    user = UserInfoSerializer(many=False)
    og_comment_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_og_comment_owner(self, obj):
        c_serializer = CommentSerializer(obj)
        user_id = c_serializer.data["og_comment_owner"]
        if user_id is not None:
            user = User.objects.get(id=user_id)
            u_serializer = UserInfoSerializer(user)
            return u_serializer.data["username"]
        else:
            return None
