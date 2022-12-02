from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
    path("user/", retrieve_update_user_view, name="user"),
    path("<str:me>/<str:user>/follow/", follow_user_view, name="follow_user"),
    path("<str:username>/followers/", get_user_followers_view, name="user_followers"),
    path("<str:username>/following/", get_user_following_view, name="user_following"),
    # path("<str:username>/block", views.Block_user),
    path("logout/", logout_user_view, name="logout_user"),
    # third party package urls
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
