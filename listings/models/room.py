from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _

from base.models import UUIDMixin
from listings.models.listing import Listing


class BedType(models.IntegerChoices):
    """An enum of bed type choices."""
    SINGLE = 1, _('Single')
    DOUBLE = 2, _('Double')
    QUEEN = 3, _('Queen')
    KING = 4, _('King')


class Room(UUIDMixin):
    """The model to represent one available room in a listing."""
    listing = ForeignKey(
        Listing,
        related_name='rooms',
        on_delete=models.CASCADE,
        help_text=_('The listing that this room belongs to.')
    )
    bed_type = models.IntegerField(
        default=BedType.SINGLE,
        choices=BedType.choices,
        help_text=_('The type of bed that this room is equipped with.')
    )
    ensuite = models.BooleanField(
        default=False,
        help_text=_('A boolean to indicate whether or not this room has '
                    'an ensuite bathroom.')
    )
    minifridge = models.BooleanField(
        default=False,
        help_text=_('A boolean to indicate whether or not this room comes with '
                    'a mini-fridge.')
    )

    def __str__(self):
        """A human readable representation of a room."""
        output = f'Bed: {BedType(self.bed_type).label}, ' \
                 f'Ensuite: [{"✔" if self.ensuite else "✗"}] ' \
                 f'Minifridge: [{"✔" if self.minifridge else "✗"}] ' \
                 f'for listing: {self.listing_id} '
        return output
