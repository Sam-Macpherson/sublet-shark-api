"""Views for the institutions app."""

from rest_framework import viewsets
from rest_framework.response import Response

from institutions.models import Institution
from institutions.serializers import InstitutionSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Institution model."""
    queryset = Institution.objects.all().prefetch_related('domains')
    serializer_class = InstitutionSerializer
