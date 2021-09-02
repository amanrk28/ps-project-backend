from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AuthToken, User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    search_fields = ('first_name', 'username', 'email', 'phone_number__startswith')
    list_display = ('email', 'phone_number', 'username', 'is_admin', 'is_store_owner')
    list_filter = ('is_admin', 'is_store_owner')
    readonly_fields = ('created_at', 'date_joined')
    fieldsets = (
        ('Basics', {'fields': (
            'email', 'phone_number', 'password', 'first_name', 'last_name', 'username', 'address',
            'is_admin', 'is_active', 'is_store_owner')}),
        ('Permissions', {
            'classes': ('collapse',), 'fields': ('user_permissions', 'groups')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type')

@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user',)