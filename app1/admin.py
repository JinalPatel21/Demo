from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ('id', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {"fields": ('is_active', 'is_superuser',)}),)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                'email',
                'is_active', 'is_superuser',
            ),
        },),)
    list_display = ['id', 'email',
                    'is_active', 'is_superuser', 'last_login']
    search_fields = ['email']
    ordering = ['-id']


