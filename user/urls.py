from django.urls import path
from .views import (
    retrieve_update_user_view,
    check_username_view,
    get_user_details_view,
    follow_user_view,
    get_user_followers_view,
    get_user_following_view,
    save_post_view,
    block_user_view,
    get_blocked_users_view,
)

app_name = "user"


urlpatterns = [
    path("", retrieve_update_user_view, name="retrieve_update_user"),
    path("detail/<str:username>/", get_user_details_view, name="get_user_details"),
    path("follow/<str:username>/", follow_user_view, name="follow_user"),
    path("check/<str:username>/", check_username_view, name="check_username"),
    path("save-post/<str:post_id>/", save_post_view, name="save_post"),
    path("followers/<str:username>/", get_user_followers_view, name="user_followers"),
    path("following/<str:username>/", get_user_following_view, name="user_following"),
    path("block/<str:username>/", block_user_view, name="block_user"),
    path("blocked/", get_blocked_users_view, name="blocked_users"),
]
