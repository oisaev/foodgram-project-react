from django.contrib import admin

from .models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


admin.site.register(User)
admin.site.register(Subscription)
