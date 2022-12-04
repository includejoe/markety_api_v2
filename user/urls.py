from django.urls import path
from .views import (
    register_user_view,
    login_user_view,
    retrieve_update_user_view,
    logout_user_view,
    follow_user_view,
    get_user_followers_view,
    get_user_following_view,
    block_user_view,
    get_blocked_users_view,
)

app_name = "user"


urlpatterns = [
    path("register/", register_user_view, name="register_user"),
    path("login/", login_user_view, name="login_user"),
    path("", retrieve_update_user_view, name="retrieve_update_user"),
    path("follow/<str:username>/", follow_user_view, name="follow_user"),
    path("followers/<str:username>/", get_user_followers_view, name="user_followers"),
    path("following/<str:username>/", get_user_following_view, name="user_following"),
    path("block/<str:username>/", block_user_view, name="block_user"),
    path("blocked/", get_blocked_users_view, name="blocked_users"),
    path("logout/", logout_user_view, name="logout_user"),
]
