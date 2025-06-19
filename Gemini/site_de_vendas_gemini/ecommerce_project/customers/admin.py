# customers/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomerProfile

# Desregistra o UserAdmin padrão para poder estendê-lo
admin.site.unregister(User)

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'perfil'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (CustomerProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__phone_number')

    def get_phone_number(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else ''
    get_phone_number.short_description = 'Telefone'