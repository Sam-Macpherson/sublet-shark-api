from django.urls import path, include
from rest_framework import routers

from listings.views import ListingViewSet

router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')


urlpatterns = [
    path('', include(router.urls))
]
