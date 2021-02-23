"""Views for the listings app."""

from rest_framework import viewsets

from listings.filters import ListingFilter
from listings.models import Listing
from listings.serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Listing model."""
    queryset = Listing.objects.all().prefetch_related('images').distinct()
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
