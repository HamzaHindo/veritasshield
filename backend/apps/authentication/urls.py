from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import CustomLoginView, LogoutView, RegisterView

urlpatterns = [
    path("login/", CustomLoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("register/", RegisterView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    # path("google-login/", CustomLoginView.as_view(), name="google_login"), #Further implementation needed for Google OAuth2 login
]
