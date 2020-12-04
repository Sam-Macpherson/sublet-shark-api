"""Views for the listings app."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from listings.filters import ListingFilter
from listings.models import Listing
from listings.serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Listing model."""
    queryset = Listing.objects.all().prefetch_related('images').distinct()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    filter_class = ListingFilter
