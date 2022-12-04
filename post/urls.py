from django.urls import path
from .views import (
    create_post_view,
    get_user_posts_view,
    post_detail_view,
    get_all_posts_view,
    like_post_view,
)

app_name = "post"

urlpatterns = [
    path("", get_all_posts_view, name="get_all_posts"),
    path("create/", create_post_view, name="create_post"),
    path("user/<str:username>/", get_user_posts_view, name="get_user_posts"),
    path("<str:post_id>/", post_detail_view, name="post_detail"),
    path("like/<str:post_id>/", like_post_view, name="like_post"),
]
