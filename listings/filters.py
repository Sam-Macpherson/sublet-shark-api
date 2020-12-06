"""Filter classes for the listings app."""
from django import forms
from django_filters import rest_framework as filters

from base.filters import NumberInFilter
from listings.models import Listing


class ListingFilter(filters.FilterSet):
    start_date = filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte',
    )
    end_date = filters.DateFilter(
        field_name='end_date',
        lookup_expr='lte',
    )
    ensuite = filters.BooleanFilter(
        field_name='rooms__ensuite',
        lookup_expr='exact',
    )
    minifridge = filters.BooleanFilter(
        field_name='rooms__minifridge',
        lookup_expr='exact',
    )
    bed_type = NumberInFilter(
        field_name='rooms__bed_type',
        lookup_expr='in',
    )

    class Meta:
        model = Listing
        fields = [
            'start_date',
            'end_date',
            'ensuite',
            'minifridge',
            'bed_type',
        ]
