"""Serializers for the listings app."""

from rest_framework import serializers

from listings.models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='image')

    class Meta:
        model = ListingImage
        exclude = ['listing', 'image']


class ListingSerializer(serializers.ModelSerializer):
    term_length = serializers.IntegerField(read_only=True)
    images = ListingImageSerializer(many=True, required=False)

    class Meta:
        model = Listing
        fields = '__all__'
