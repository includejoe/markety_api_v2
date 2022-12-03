import uuid
from django.db import models
from user.models import User
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class Post(models.Model):
    CONDITION_CHOICES = (("new", "new"), ("used", "used"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default=None)
    image1 = models.URLField()
    image2 = models.URLField()
    image3 = models.URLField()
    is_sold = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(default=timezone.now)
    body = models.TextField(max_length=1000)
    likes = models.ManyToManyField(User, related_name="liked_comments")
