from django.urls import path
from .views import (
    create_comment_view,
    get_post_comments_view,
    like_comment_view,
    comment_detail_view,
)

app_name = "comment"

urlpatterns = [
    path("create/", create_comment_view, name="create_comment"),
    path("<str:post_id>/", get_post_comments_view, name="post_comments"),
    path("like/<str:comment_id>/", like_comment_view, name="like_comment"),
    path("detail/<str:comment_id>/", comment_detail_view, name="comment_detail"),
]
