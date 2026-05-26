from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'email', 'account_status', 'is_staff')
    list_filter = ('account_status', 'is_staff')
    search_fields = ('phone_number', 'email')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Status', {'fields': ('account_status', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password1', 'password2')}),
    )
