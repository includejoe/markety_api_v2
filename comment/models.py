import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    replies = models.ManyToManyField("self", blank=True, symmetrical=False)
    is_reply = models.BooleanField(default=False)
    og_comment_owner = models.ForeignKey(
        User, on_delete=models.Case, blank=True, null=True
    )

    # Check if comment is a reply and then add og_comment_owner
    def clean(self):
        if self.is_reply is True and self.og_comment_owner is None:
            raise ValidationError(
                {"og_comment_owner": "This field is required when is_reply is true"}
            )
