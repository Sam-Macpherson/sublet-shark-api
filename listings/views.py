"""Views for the listings app."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from listings.models import Listing
from listings.serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Listing model."""
    queryset = Listing.objects.all().prefetch_related('images')
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
