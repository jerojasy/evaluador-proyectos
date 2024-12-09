from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Roles y permisos', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active'),
        }),
    )
