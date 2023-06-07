from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Модель настройки User в панели администратора."""
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
