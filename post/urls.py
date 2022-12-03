from django.urls import path
from .views import create_post_view, get_user_posts_view, post_detail_view

app_name = "post"

urlpatterns = [
    path("create/", create_post_view, name="create_post"),
    path("<str:username>/posts/", get_user_posts_view, name="get_user_posts"),
    path("<str:post_id>/", post_detail_view, name="post_detail_view"),
]
