import uuid

from django.db import models
from django.db.models import UUIDField


class UUIDMixin(models.Model):
    id = UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
