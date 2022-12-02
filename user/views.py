from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveUpdateAPIView


from rest_framework.decorators import api_view


from . import serializers
from .models import User

# api/v1/register/
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

# api/v1/login/
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

# api/v1/user/
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


class FollowUser(APIView):
    serializer_class = serializers.FollowingSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, me, user):
        if me == user:
            raise ParseError(detail="User cannot follow itself", code=400)

        current_user = User.objects.get(username=me)
        user_to_follow = User.objects.get(username=user)

        if current_user is None or user_to_follow is None:
            raise ParseError(detail="Invalid data", code=400)

        already_followed = current_user.following.filter(username=user).exists()

        if already_followed:
            current_user.following.remove(user_to_follow)
        else:
            current_user.following.add(user_to_follow)

        current_user.save()
        serializer = self.serializer_class(current_user)

        return Response(serializer.data, status=status.HTTP_200_OK)


follow_user_view = FollowUser.as_view()


# api/v1/<str:username>/followers
class GetUserFollowers(APIView):
    serializer_class = serializers.FollowersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)

        if user is None:
            raise ParseError(detail="Invalid data", code=400)

        followers = user.followers.all()

        serializer = self.serializer_class(followers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_followers_view = GetUserFollowers.as_view()


# api/v1/<str:username>/following
class GetUserFollowing(APIView):
    serializer_class = serializers.FollowingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)

        if user is None:
            raise ParseError(detail="Invalid data", code=400)

        following = user.following.all()
        serializer = self.serializer_class(following, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_following_view = GetUserFollowing.as_view()


# Blocked Logic
# api/v1/<str:username>/block
# @api_view(['PUT'])
# def Block_user(request,username):
#     '''
#     Purpose: Block the user
#     Input: -
#     Output: Blocked user
#     '''
#     try:
#         user = TUser.objects.get(username=username)
#         user.blocked = True
#         user.save()
#         serializer = TUserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         error = {'Error_code': status.HTTP_400_BAD_REQUEST,
#                         'Error_Message': "User does not exist"}
#         logger.error(e)
#         return Response(error, status=status.HTTP_400_BAD_REQUEST)


# api/v1/logout/
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
