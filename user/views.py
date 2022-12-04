from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, APIException
from rest_framework.generics import RetrieveUpdateAPIView


from base.utils import jwt_decode


from . import serializers
from .models import User

# user/register/
class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        # Return user response after a successful registration
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


register_user_view = RegistrationAPIView.as_view()

# user/login/
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        # Return user after login
        user = request.data
        serializer = self.serializer_class(data=user)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


login_user_view = LoginAPIView.as_view()

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

# user/follow/<str:user>/
class FollowUser(APIView):
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
            raise ParseError(detail=e, code=400)


follow_user_view = FollowUser.as_view()


# user/followers/<str:username>/
class GetUserFollowers(APIView):
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
class GetUserFollowing(APIView):
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
class BlockUser(APIView):
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
            raise ParseError(detail=e, code=400)


block_user_view = BlockUser.as_view()


class GetBlockedUsers(APIView):
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


# user/logout/
class LogoutAPIView(APIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate token and save
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


logout_user_view = LogoutAPIView.as_view()
