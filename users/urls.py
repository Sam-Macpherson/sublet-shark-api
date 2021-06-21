"""URLs for the users app."""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, BlacklistTokenView, EmailVerificationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_access_token'),
    path('activate/<uidb64>/<token>', EmailVerificationView.as_view(), name='activate')
]
