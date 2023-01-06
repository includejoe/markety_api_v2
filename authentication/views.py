from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


from . import serializers

# Create your views here.
class RegistrationAPIView(GenericAPIView):
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


class LoginAPIView(GenericAPIView):
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


class LogoutAPIView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate token and save
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


logout_user_view = LogoutAPIView.as_view()
