"""URLs for the users app."""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, BlacklistTokenView, EmailVerificationView, ResetPasswordView, UserProfileView

urlpatterns = [
    path('<uid>/profile/', UserProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_access_token'),
    path('reset-password/<uidb64>/<token>', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('activate/<uidb64>/<token>', EmailVerificationView.as_view(), name='activate'),
]
