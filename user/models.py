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
        username,
        email,
        gender,
        dob,
        phone,
        password=None,
        is_staff=False,
        is_superuser=False,
    ):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.dob = dob
        user.phone = phone
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(
        self, first_name, last_name, username, email, gender, dob, phone, password
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            gender=gender,
            dob=dob,
            phone=phone,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (("male", "male"), ("female", "female"), ("other", "other"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=255, default="+233")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Other")
    dob = models.DateField(null=True)
    bio = models.TextField(null=True)
    location = models.CharField(max_length=255, null=True)
    profile_image = models.ImageField(null=True)
    cover_image = models.ImageField(null=True)
    is_vendor = models.BooleanField(default=False)
    bus_name = models.CharField(max_length=255, blank=True, null=True)
    bus_category = models.CharField(max_length=255, null=True)
    bus_website = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    blocked_users = models.ManyToManyField(
        "self",
        related_name="blocked_by",
        symmetrical=False,
    )
    following = models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "dob", "gender", "phone"]

    objects = UserManager()

    @property
    def tokens(self):
        # Allow us to get a user's token by calling `user.token`
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def get_full_name(self):
        # Return full name of user
        return self.first_name + self.last_name
