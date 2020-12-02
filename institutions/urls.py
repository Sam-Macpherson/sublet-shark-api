"""URLs for the institutions app."""

from django.urls import path, include
from rest_framework import routers

from institutions.views import InstitutionViewSet

router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet, basename='listing')


urlpatterns = [
    path('', include(router.urls))
]
