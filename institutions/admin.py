from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django_admin_relation_links import AdminChangeLinksMixin

from institutions.models import Institution, Domain


@admin.register(Domain)
class DomainAdmin(AdminChangeLinksMixin, ModelAdmin):
    """Manage the Domain model."""
    list_display = (
        'domain',
        'institution_link',
    )
    change_links = (
        'institution',
    )
    search_fields = (
        'institution',
        'id',
        'domain',
    )


@admin.register(Institution)
class InstitutionAdmin(ModelAdmin):
    """Manage the Institution model."""
    list_display = (
        'name',
        'address',
    )
    search_fields = (
        'name',
        'address',
    )
