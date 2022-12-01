from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    register_user_view,
    login_user_view,
    retrieve_update_user_view,
    logout_user_view,
)

app_name = "user"

urlpatterns = [
    path("register/", register_user_view, name="register_user"),
    path("login/", login_user_view, name="login_user"),
    path("user/", retrieve_update_user_view, name="user"),
    path("logout/", logout_user_view, name="logout_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
