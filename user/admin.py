# admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'name', 'is_active', 'is_staff')
    search_fields = ('username', 'name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)






User = get_user_model()

class ReadOnlyAdmin(BaseUserAdmin):
    # Set all fields to read-only
    readonly_fields = [field.name for field in User._meta.fields]

    # Disable adding users
    def has_add_permission(self, request):
        return False

    # Allow viewing the change form, but fields will be read-only
    def has_change_permission(self, request, obj=None):
        return True

    # Disable deleting users
    def has_delete_permission(self, request, obj=None):
        return False

    # Remove the delete action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

# Unregister the existing User admin
admin.site.unregister(User)

# Register the User model with the ReadOnlyAdmin class
admin.site.register(User, ReadOnlyAdmin)

