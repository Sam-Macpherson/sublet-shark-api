from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """Filters based on the logic:

    "If the number is in this set of numbers: 1,2,3". Behaves identically
    to BaseInFilter except enforces Number type.
    """
    pass
