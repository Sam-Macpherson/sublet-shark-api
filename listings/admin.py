from django.contrib import admin
from .models import Listing, Room, ListingImage

admin.site.register(Room)
admin.site.register(ListingImage)
admin.site.register(Listing)
