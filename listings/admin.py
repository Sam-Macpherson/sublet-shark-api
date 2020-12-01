from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django_admin_relation_links import AdminChangeLinksMixin

from listings.models import Listing, ListingImage, Room


@admin.register(Listing)
class ListingAdmin(ModelAdmin):
    """Manage the Listings model."""
    list_display = [
        'address',
        'accommodation_type',
        'term_length',
        'start_date',
        'end_date',
    ]
    search_fields = [
        'address',
        'id',
    ]


@admin.register(ListingImage)
class ListingImageAdmin(AdminChangeLinksMixin, ModelAdmin):
    """Manage the ListingImage model."""
    list_display = [
        'filename',
        'listing_link',
        'image',
        'uploaded_at',
    ]
    change_links = [
        'listing',
    ]
    search_fields = [
        'filename',
        'listing__id',
        'listing__address',
    ]

    @staticmethod
    def listing_link_label(listing):
        return f'{listing.address}'


@admin.register(Room)
class RoomAdmin(AdminChangeLinksMixin, ModelAdmin):
    """Manage the Room model."""
    list_display = [
        'bed_type',
        'listing_link',
        'ensuite',
        'minifridge',
    ]
    change_links = [
        'listing',
    ]

    @staticmethod
    def listing_link_label(listing):
        return f'{listing.address}'

