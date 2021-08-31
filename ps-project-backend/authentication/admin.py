from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    search_fields = ('first_name', 'email', 'phone_number')
    list_display = ('username', 'phone_number', 'email', 'is_admin', 'is_store_owner')
    list_filter = ('is_admin', 'is_store_owner')
    readonly_fields = ('created_on', 'date_joined' )
    fieldsets = (
        ('Basics', {'fields': (
            'is_active', 'email', 'phone_number', 'password', 'first_name', 'last_name', 'username', 'is_admin',
            'is_store_owner', 'address')}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

