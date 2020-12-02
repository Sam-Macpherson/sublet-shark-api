"""Serializers for the institutions app."""

from rest_framework import serializers

from institutions.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
    """Serializer for the Institution model."""
    domains = serializers.SerializerMethodField()

    class Meta:
        model = Institution
        exclude = ('id', )

    @staticmethod
    def get_domains(institution):
        return [domain.domain for domain in institution.domains.all()]
