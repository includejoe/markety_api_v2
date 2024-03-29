from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, APIException
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.views import APIView

from base.utils import jwt_decode
from post.models import Post
from . import serializers
from .models import User
from .utils import is_username_valid


# user/
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Return user on get request
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Return updated user
        user = request.data
        serializer = self.serializer_class(
            request.user,
            data=user,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


retrieve_update_user_view = UserRetrieveUpdateAPIView.as_view()


class CheckUsername(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        valid, error_message = is_username_valid(username)

        if not valid:
            raise ParseError(detail=error_message)

        username_exists = User.objects.filter(username=username).exists()

        if username_exists:
            return Response({"available": False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"available": True}, status=status.HTTP_200_OK)


check_username_view = CheckUsername.as_view()


class GetUserDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserPublicSerializer

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ParseError(detail=e, code=401)


get_user_details_view = GetUserDetails.as_view()


class SavePost(GenericAPIView):
    serializer_class = serializers.SavePostSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, post_id):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        user = User.objects.get(id=user_id)

        try:
            post = Post.objects.get(id=post_id)
            already_saved = user.saved_posts.filter(id=post_id).exists()

            if already_saved:
                user.saved_posts.remove(post)
            else:
                user.saved_posts.add(post)

            user.save()
            serializer = self.serializer_class(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


save_post_view = SavePost.as_view()

# user/follow/<str:user>/
class FollowUser(GenericAPIView):
    serializer_class = serializers.FollowUserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, username):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        current_user = User.objects.get(id=user_id)

        try:
            user_to_follow = User.objects.get(username=username)
        except Exception as e:
            raise ParseError(detail=e)

        if current_user.id == user_to_follow.id:
            raise ParseError(detail="User cannot follow itself", code=400)

        try:
            already_followed = current_user.following.filter(username=username).exists()

            if already_followed:
                current_user.following.remove(user_to_follow)
            else:
                current_user.following.add(user_to_follow)

            current_user.save()
            serializer = self.serializer_class(current_user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


follow_user_view = FollowUser.as_view()


# user/followers/<str:username>/
class GetUserFollowers(GenericAPIView):
    serializer_class = serializers.FollowersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except:
            raise ParseError(detail="Username not found", code=404)

        followers = user.followers.all()

        serializer = self.serializer_class(followers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_followers_view = GetUserFollowers.as_view()


# user/<str:username>/following
class GetUserFollowing(GenericAPIView):
    serializer_class = serializers.FollowingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except:
            raise ParseError(detail="Username not found", code=404)

        following = user.following.all()
        serializer = self.serializer_class(following, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_following_view = GetUserFollowing.as_view()

# user/block/<str:username>/
class BlockUser(GenericAPIView):
    serializer_class = serializers.BlockUserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, username):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        current_user = User.objects.get(id=user_id)

        try:
            user_to_block = User.objects.get(username=username)
        except Exception as e:
            raise ParseError(detail=e)

        if current_user.id == user_to_block.id:
            raise ParseError(detail="User cannot block itself", code=400)

        try:
            already_blocked = current_user.blocked_users.filter(
                username=username
            ).exists()

            if already_blocked:
                current_user.blocked_users.remove(user_to_block)
            else:
                current_user.blocked_users.add(user_to_block)

            current_user.save()
            serializer = self.serializer_class(current_user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


block_user_view = BlockUser.as_view()


class GetBlockedUsers(GenericAPIView):
    serializer_class = serializers.BlockedUsersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers["AUTHORIZATION"]
        user_id = jwt_decode(token)
        user = User.objects.get(id=user_id)
        try:
            blocked = user.blocked_users.all()
            serializer = self.serializer_class(blocked, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


get_blocked_users_view = GetBlockedUsers.as_view()
