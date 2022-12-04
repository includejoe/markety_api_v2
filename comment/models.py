import uuid
from django.utils import timezone
from django.db import models

from user.models import User
from post.models import Post


# Create your models here.
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(default=timezone.now)
    body = models.TextField(max_length=1000)
    likes = models.ManyToManyField(User, related_name="liked_comments")
