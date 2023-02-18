import uuid
from django.db import models
from user.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    is_new = models.BooleanField(default=True)
    image1 = models.URLField()
    image2 = models.URLField()
    image3 = models.URLField()
    is_sold = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    saved_by = models.ManyToManyField(User, related_name="saved_posts", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
