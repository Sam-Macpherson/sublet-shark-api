from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import UUIDMixin


class Institution(UUIDMixin):
    """The model to represent an institution whose members may create
    accounts.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of the institution, i.e. University of Waterloo.')
    )
    address = models.CharField(
        max_length=255,
        help_text=_('The street address of the institution.')
    )

    def __str__(self):
        """Human readable representation of the institution."""
        return self.name


class Domain(UUIDMixin):
    """The model to represent a domain address of an institution."""
    institution = models.ForeignKey(
        Institution,
        related_name='domains',
        on_delete=models.CASCADE,
        help_text=_('The institution that this domain is for.')
    )
    domain = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The actual domain of an institution\'s email address, for '
                    'example: uwaterloo.ca')
    )

    def __str__(self):
        """Human readable representation of the domain."""
        return self.domain
