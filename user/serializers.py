from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .models import User
from .utils import is_email_valid, is_username_valid


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
            "is_vendor",
            "bus_name",
            "bus_category",
            "bus_location",
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
        return "@" + value

    def create(self, validated_data):
        # Return user after creation

        # cross check with og code on dev.io if error
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        # Get user tokens
        user = User.objects.get(email=obj.email)
        return {"refresh": user.tokens["refresh"], "access": user.tokens["access"]}

    class Meta:
        model = User
        fields = ["email", "username", "password", "tokens", "is_staff"]

    def validate(self, data):
        # Validate and return user login
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required")

        if password is None:
            raise serializers.ValidationError("A password is required")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("This user is currently deactivated")

        return user


class UserSerializer(serializers.ModelSerializer):
    # Handle serialization and deserialization of User objects
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = []
