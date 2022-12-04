from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, APIException

from base.utils import jwt_decode
from .serializers import CommentSerializer
from .models import Comment


# Create your views here.
class PostComments(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, post_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)

        comment_data = {**request.data, "post": post_id, "user": user_id}
        serializer = self.serializer_class(data=comment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


post_comments_view = PostComments.as_view()
