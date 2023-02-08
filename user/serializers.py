from rest_framework import serializers

from .models import User
from .utils import is_username_valid


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
            "is_verified",
            "posts",
            "followers",
            "following",
            "created_at",
        ]

        read_only_fields = [
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

        return


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "bus_name",
            "is_vendor",
            "is_verified",
            "profile_image",
        ]


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "bio",
            "bus_name",
            "bus_category",
            "bus_website",
            "profile_image",
            "cover_image",
            "is_vendor",
            "is_verified",
            "following",
            "followers",
            "is_active",
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
