from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .models import User
from .utils import is_email_valid, is_username_valid


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "profile_image",
            "cover_image",
            "is_vendor",
            "is_verified",
        ]


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["following"]


class BlockedUsersSerializer(serializers.ModelSerializer):
    blocked_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["blocked_users"]

    def get_blocked_users(self, obj):
        users = User.objects.get(id=obj.id)
        serializer = UserPublicSerializer(users)
        return serializer.data


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["blocked_users"]


class FollowersSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["followers"]

    def get_followers(self, obj):
        users = User.objects.get(id=obj.id)
        serializer = UserPublicSerializer(users)
        return serializer.data


class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["following"]

    def get_following(self, obj):
        users = User.objects.get(id=obj.id)
        serializer = UserPublicSerializer(users)
        return serializer.data


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    # tokens = serializers.SerializerMethodField()

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
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "phone",
            "gender",
            "dob",
            "bio",
            "location",
            "profile_image",
            "cover_image",
            "is_vendor",
            "bus_name",
            "bus_category",
            "bus_website",
            "is_active",
            "is_staff",
            "is_verified",
            "posts",
            "blocked_users",
            "followers",
            "country",
            "created_at",
            "updated_at",
            "tokens",
        ]

        read_only_fields = [
            "tokens",
            "is_staff",
            "id",
            "is_verified",
        ]

    def update(self, instance, validated_data):
        # Perform an update on a user
        password = validated_data.get("password", None)
        username = validated_data.get("username", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        if username is not None:
            valid, error_message = is_username_valid(username)
            if not valid:
                raise serializers.ValidationError(error_message)

        instance.save()

        return instance


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
