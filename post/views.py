from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ParseError, APIException

from base.utils import jwt_decode, delete_success
from .serializers import PostSerializer
from .models import Post
from user.models import User


invalid_post_id = "Invalid post ID"


# posts/create
class CreatePost(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        post_data = request.data
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)

        try:
            user = User.objects.get(id=user_id)
            post_data["user"] = user
            new_post = Post(**post_data)
            new_post.save()
        except:
            raise ParseError(detail="No user with this username found", code=400)

        serializer = self.serializer_class(new_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


create_post_view = CreatePost.as_view()

# posts/user/<str:username>/
class GetUserPosts(GenericAPIView):
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


# posts/<str:post_id>/
class PostDetail(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    # GET REQUEST
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            raise ParseError(detail=invalid_post_id, code=401)

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
            raise ParseError(detail=invalid_post_id)

        if post_to_delete.user.id != post_owner.id:
            raise ParseError(detail="User does not own this post", code=401)

        try:
            post_to_delete.delete()
            return Response(delete_success, status=status.HTTP_200_OK)
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
            raise ParseError(detail=invalid_post_id)

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

# posts/
class GetALlPosts(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def get(self, request):
        try:
            # TODO: implement more functionality and return posts based on which user is logged in
            posts = Post.objects.all()
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


get_all_posts_view = GetALlPosts.as_view()

# posts/like/<str:post_id>/
class LikePost(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def patch(self, request, post_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        post_liker = User.objects.get(id=user_id)

        try:
            post_to_like = Post.objects.get(id=post_id)
        except Exception as e:
            raise ParseError(detail=invalid_post_id)

        try:
            already_liked = post_to_like.likes.filter(id=post_liker.id).exists()
            if already_liked:
                post_to_like.likes.remove(post_liker)
            else:
                post_to_like.likes.add(post_liker)

            serializer = self.serializer_class(post_to_like)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


like_post_view = LikePost.as_view()
