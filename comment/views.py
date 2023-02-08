from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ParseError, APIException

from base.utils import jwt_decode, delete_success
from .serializers import (
    CreateCommentSerializer,
    CommentSerializer,
    GetCommentSerializer,
)
from .models import Comment
from user.models import User
from post.models import Post


invalid_comment_id = "Invalid comment ID"


# comments/create/
class CreateComment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer

    def post(self, request):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)

        comment_data = {**request.data, "user": user_id}
        serializer = self.serializer_class(data=comment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


create_comment_view = CreateComment.as_view()


class ReplyComment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer

    def patch(self, request, comment_id):
        post_id = request.data["post"]
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)

        try:
            user = User.objects.get(id=user_id)
            post = Post.objects.get(id=post_id)
            request.data["post"] = post
            reply = Comment(**request.data, user=user, is_reply=True)
            reply.save()

            comment_to_reply = Comment.objects.get(id=comment_id)
            comment_to_reply.replies.add(reply)

            serializer = self.serializer_class(reply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


reply_comment_view = ReplyComment.as_view()

# comments/<str:post_id>/
class GetPostComments(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetCommentSerializer

    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_post_comments_view = GetPostComments.as_view()

# comments/like/<str:comment_id>/
class LikeComment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def patch(self, request, comment_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        comment_liker = User.objects.get(id=user_id)

        try:
            comment_to_like = Comment.objects.get(id=comment_id)
        except Exception as e:
            raise ParseError(detail=invalid_comment_id)

        try:
            already_liked = comment_to_like.likes.filter(id=comment_liker.id).exists()
            if already_liked:
                comment_to_like.likes.remove(comment_liker)
            else:
                comment_to_like.likes.add(comment_liker)

            serializer = self.serializer_class(comment_to_like)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


like_comment_view = LikeComment.as_view()

# comments/<str:comment_id>/
class CommentDetail(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def delete(self, request, comment_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        comment_owner = User.objects.get(id=user_id)

        try:
            comment_to_delete = Comment.objects.get(id=comment_id)
        except Exception as e:
            raise ParseError(detail=invalid_comment_id)

        if comment_to_delete.user.id != comment_owner.id:
            raise ParseError(detail="User does not own this post", code=401)

        try:
            comment_to_delete.delete()
            return Response(delete_success, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


comment_detail_view = CommentDetail.as_view()
