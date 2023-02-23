from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    saved_artists = models.ManyToManyField('music.Artist', blank=True, related_name='+', verbose_name='Saved Artist(s)')
    saved_albums = models.ManyToManyField('music.Album', blank=True, related_name='+', verbose_name='Saved Album(s)')
    favorite_songs = models.ManyToManyField('music.Song', blank=True, related_name='+', verbose_name='Favorite Song(s)')
