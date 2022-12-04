from django.urls import path
from .views import (
    register_user_view,
    login_user_view,
    retrieve_update_user_view,
    logout_user_view,
    follow_user_view,
    get_user_followers_view,
    get_user_following_view,
)

app_name = "user"


urlpatterns = [
    path("register/", register_user_view, name="register_user"),
    path("login/", login_user_view, name="login_user"),
    path("", retrieve_update_user_view, name="retrieve_update_user"),
    path("follow/<str:me>/<str:user>/", follow_user_view, name="follow_user"),
    path("followers/<str:username>/", get_user_followers_view, name="user_followers"),
    path("following/<str:username>/", get_user_following_view, name="user_following"),
    # path("<str:username>/block", views.Block_user),
    path("logout/", logout_user_view, name="logout_user"),
]
