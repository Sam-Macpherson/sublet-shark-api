from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'profile_picture', 'bio', 'sublet_status')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'profile_picture', 'sublet_status')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):

    # TODO REMOVE THIS CUSTOM BEHAVIOUR (IT IS ONLY FOR TESTING)
    def has_delete_permission(self, *args, **kwargs): return True


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)
