from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'role', 'is_active',)
    list_filter = ('phone_number', 'is_active', 'email',)
    search_fields = ('email', 'first_name', 'last_name',)
