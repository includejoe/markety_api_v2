from django.urls import path
from .views import post_comments_view

app_name = "comment"

urlpatterns = [
    path("<str:post_id>/", post_comments_view, name="comments"),
]
