from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

app_name = "users"

urlpatterns = (
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password/reset/", views.ResetPasswordView.as_view(), name="password_reset"),
)
