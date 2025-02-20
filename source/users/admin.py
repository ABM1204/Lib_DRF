from django.contrib import admin

from users.models import User

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name')

