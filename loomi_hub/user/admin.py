from django.contrib import admin

from loomi_hub.user.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')