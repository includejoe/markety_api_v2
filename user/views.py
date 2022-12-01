from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import UserJSONRenderer
from . import serializers


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserJSONRenderer]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        # Return user response after a successful registration
        user_request = request.data.get("user", {})
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


register_user_view = RegistrationAPIView.as_view()


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserJSONRenderer]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        # Return user after login
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


login_user_view = LoginAPIView.as_view()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserJSONRenderer]
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Return user on get request
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Return updated user
        serializer_data = request.data.get("user", {})
        serializer = self.serializer_class(
            request.user,
            data=serializer_data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


retrieve_update_user_view = UserRetrieveUpdateAPIView.as_view()


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
