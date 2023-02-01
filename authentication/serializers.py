from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from user.models import User
from user.utils import is_email_valid, is_username_valid


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "phone",
            "gender",
            "dob",
            "location",
            "is_vendor",
            "bus_name",
            "bus_category",
        ]

    def validate_email(self, value):
        # Normalize and validate email address
        valid, error_message = is_email_valid(value)
        if not valid:
            raise serializers.ValidationError(error_message)
        try:
            email_name, domain = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain.lower()])

        return value

    def validate_username(self, value):
        valid, error_message = is_username_valid(value)
        if not valid:
            raise serializers.ValidationError(error_message)
        return value

    def create(self, validated_data):
        # Return user after creation
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    jwt = serializers.SerializerMethodField()

    def get_jwt(self, obj):
        # Get user tokens
        user = User.objects.get(username=obj.username)
        return user.tokens["access"]

    class Meta:
        model = User
        fields = ["username", "password", "jwt"]

    def validate(self, data):
        # Validate and return user login
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise serializers.ValidationError("A username is required")

        if password is None:
            raise serializers.ValidationError("A password is required")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("This user is currently deactivated")

        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        # Validate token
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        # Validate save blacklisted token
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)
