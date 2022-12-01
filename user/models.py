import uuid
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,
        phone,
        gender,
        password=None,
        is_staff=False,
        is_superuser=False,
    ):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not gender:
            raise ValueError("User must have a gender")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, first_name, last_name, email, phone, password, gender):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            gender=gender,
            is_staff=True,
            is_superuser=True,
        )
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Other"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=255, default="+233  ")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="O")
    dob = models.DateField(null=True)
    bio = models.TextField(null=True)
    profile_image = models.URLField(null=True)
    cover_image = models.URLField(null=True)
    is_vendor = models.BooleanField(default=False)
    bus_name = models.CharField(max_length=255, blank=True, null=True)
    bus_category = models.CharField(max_length=255, null=True)
    bus_location = models.CharField(max_length=255, null=True)
    bus_website = models.URLField(null=True)
    followers = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    @property
    def tokens(self):
        # Allow us to get a user's token by calling `user.token`
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def get_full_name(self):
        # Return full name of user
        return self.first_name + self.last_name
