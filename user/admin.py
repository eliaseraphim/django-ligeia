from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from . models import User


class UserAdmin(_UserAdmin):
    fieldsets = (
        *_UserAdmin.fieldsets,
        ('Music', {
            'fields': ('saved_artists', 'saved_albums', 'playlists', 'favorite_songs')
        })
    )


admin.site.register(User, UserAdmin)
