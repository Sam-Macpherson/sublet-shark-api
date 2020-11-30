import calendar
import datetime

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import DateField, CharField, TextField
from django.utils.translation import gettext_lazy as _

from base.models import UUIDMixin
from listings import AVERAGE_NUMBER_OF_DAYS_IN_A_MONTH
from subletshark import settings
from subletshark.storage_backends import PublicImageStorage


class AccommodationType(models.IntegerChoices):
    """An enum of accommodation type choices."""
    APARTMENT = 1, _('Apartment')
    HOUSE = 2, _('House')
    CONDO = 3, _('Condominium')


class Listing(UUIDMixin):
    """The model to represent a sublet listing on the website."""
    accommodation_type = models.IntegerField(
        choices=AccommodationType.choices,
        default=AccommodationType.APARTMENT,
        help_text=_('The type of building the listing is for.')
    )
    start_date = DateField(
        help_text=_('The first date that the subletter may move in.')
    )
    end_date = DateField(
        help_text=_('The date by which the subletter must leave.')
    )
    address = CharField(
        max_length=255,
        help_text=_('The string representation of the address of the building '
                    'the listing is for.')
    )
    additional_info = TextField(
        blank=True,
        help_text=_('Optional additional information about the listing '
                    'that is not covered by the other fields.')
    )

    @staticmethod
    def _round_date(date: datetime.date) -> datetime.date:
        """Returns a new date object which is equal to date, but rounded to the
        nearest month.
        Example: January 14 -> January 1
                 January 16 -> February 1
                 February 14 -> February 1
        """
        half_the_days = round(calendar.monthrange(date.year, date.month)[1] / 2)
        return (date + timedelta(days=half_the_days)).replace(day=1)

    @property
    def term_length(self):
        """The length of the sublet term, in months."""
        day_difference = (self.end_date - self.start_date).days
        number_of_months = day_difference / AVERAGE_NUMBER_OF_DAYS_IN_A_MONTH
        return round(number_of_months)

    def clean(self):
        """Validate the fields."""
        if self.end_date < self.start_date:
            raise ValidationError(_('The start date must be before the end '
                                    'date of a sublet term.'))
        if self.term_length < 1:
            raise ValidationError(_('A sublet must be available for at least '
                                    'one month.'))

    def save(self, *args, **kwargs):
        """Call the clean method before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        output = ''
        if self.address:
            output += f'{self.address} '
        output += f'({str(self.start_date)} to {str(self.end_date)}) ' \
                  f'({AccommodationType(self.accommodation_type).label})'
        return output

    class Meta:
        ordering = ['start_date']


def image_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/listing_id/filename
    return f'listing_{instance.listing.id}/{instance.filename}'


def select_storage():
    return PublicImageStorage() if settings.USE_S3 else FileSystemStorage()


class ListingImage(UUIDMixin):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(
        Listing,
        related_name='images',
        on_delete=models.CASCADE,
        help_text=_('The listing that this image belongs to.')
    )
    filename = models.CharField(max_length=255)
    image = models.ImageField(
        storage=select_storage,
        upload_to=image_filename
    )

    def __str__(self):
        return f'{self.filename} for listing: {self.listing.id}'
