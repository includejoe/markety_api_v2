from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, APIException

from base.utils import jwt_decode
from .serializers import PostSerializer
from .models import Post
from user.models import User


# api/v1/post/create
class CreatePost(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        post_data = request.data
        username = post_data["user"]
        try:
            user = User.objects.get(username=username)
            post_data["user"] = user
            new_post = Post(**post_data)
            new_post.save()
        except:
            raise ParseError(detail="No user with this username found", code=400)

        serializer = self.serializer_class(new_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


create_post_view = CreatePost.as_view()

# api/v1/post/<str:username>/posts
class GetUserPosts(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            raise ParseError(detail="Invalid username")

        try:
            posts = Post.objects.filter(user=user)
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


get_user_posts_view = GetUserPosts.as_view()


# api/v1/post/delete
class PostDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    delete_success = {"detail": "Post deleted successfully"}
    invalid_post_id = "Invalid post ID"

    # GET REQUEST
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            raise ParseError(detail=self.invalid_post_id, code=401)

        try:
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)

    # DELETE REQUEST
    def delete(self, request, post_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        post_owner = User.objects.get(id=user_id)

        try:
            post_to_delete = Post.objects.get(id=post_id)
        except Exception as e:
            raise ParseError(detail=self.invalid_post_id, code=401)

        if post_to_delete.user.id != post_owner.id:
            raise ParseError(detail="User does not own this post", code=401)

        try:
            post_to_delete.delete()
            return Response(self.delete_success, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)

    # PATCH REQUEST
    def patch(self, request, post_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        post_data = request.data
        post_owner = User.objects.get(id=user_id)

        try:
            post_to_update = Post.objects.get(id=post_id)
        except Exception as e:
            raise ParseError(detail=self.invalid_post_id)

        if post_to_update.user.id != post_owner.id:
            raise ParseError(detail="User does not own this post", code=401)

        try:
            Post.objects.filter(id=post_id).update(**post_data)
            updated_post = Post.objects.get(id=post_id)
            serializer = self.serializer_class(updated_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


post_detail_view = PostDetail.as_view()
