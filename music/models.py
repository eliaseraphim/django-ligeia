from django.db import models
from django.utils import timezone


def get_artists(query_set):
    artists = ''
    for artist in query_set:
        artists += f'{artist.name}, '

    return artists.strip(', ')


class Artist(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, verbose_name='Artist Image')
    albums = models.ManyToManyField('music.Album', blank=True)
    songs = models.ManyToManyField('music.Songs', blank=True)
    featured_on = models.ManyToManyField('music.Songs', blank=True, verbose_name='Featured On')

    def __str__(self):
        return self.name


class Album(models.Model):
    TYPE_CHOICES = [
        ('Album', 'Album'),
        ('EP', 'EP'),
        ('Single', 'Single'),
    ]

    title = models.CharField(max_length=200)
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    artwork = models.ImageField(verbose_name='Album Artwork')
    duration = models.DurationField()
    released = models.DateField()

    def __str__(self):
        return self.title

    @property
    def artists(self):
        return self.songs.all()


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    songs = models.ManyToManyField('music.Song', blank=True, on_delete=models.SET_DEFAULT)
    artwork = models.ImageField(verbose_name='Playlist Artwork')
    duration = models.DurationField()
    created = models.DateTimeField(default=timezone.now)
    last_edited = models.DateTimeField(default=timezone.now, verbose_name='Last Edited')

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)
    artists = models.ManyToManyField('music.Artist', blank=True, verbose_name='Artist(s)', related_name='songs')
    features = models.ManyToManyField('music.Artist', blank=True, verbose_name='Feature(s)', related_name='featured_on')
    album = models.ForeignKey('music.Album', blank=True, on_delete=models.SET_DEFAULT, related_name='songs')
    duration = models.DurationField()
    released = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_artists(self):
        return get_artists(self.artists.all())