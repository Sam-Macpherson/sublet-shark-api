from rest_framework import viewsets
from rest_framework.response import Response

from listings.models import Listing
from listings.serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Listing model."""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def list(self, request, **kwargs):
        serializer = ListingSerializer(self.queryset, many=True)
        return Response(serializer.data)
