from django.db import models
from django.utils import timezone


def get_property_set(query_set: models.QuerySet, relation: str):
    """
    Get a ``set`` of values from a given object's property in a query set.

    :param query_set: The query set to iterate through.
    :type query_set: django.db.models.QuerySet
    :param relation: The name of the relation field that you are reading.
    :type relation: str
    :returns: A ``set`` of values from a given object's property in a query set.
    :rtype: set
    """
    if not isinstance(query_set, models.QuerySet) or not hasattr(query_set.first(), relation)
        return None

    items = set()
    for obj in query_set:
        for value in getattr(obj, relation):
            items.add(value)

    return items


class Artist(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, verbose_name='Artist Image')

    def __str__(self):
        return self.name

    @property
    def albums(self):
        return get_property_set(self.songs.all(), 'album')


class Album(models.Model):
    TYPE_CHOICES = [
        ('Album', 'Album'),
        ('EP', 'EP'),
        ('Single', 'Single'),
    ]

    title = models.CharField(max_length=200)
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    artwork = models.ImageField(blank=True, verbose_name='Album Artwork')
    duration = models.DurationField(default=0)
    released = models.DateField(blank=True)

    def __str__(self):
        return self.title

    @property
    def artists(self):
        return get_property_set(self.songs.all(), 'artists')

    @property
    def features(self):
        return get_property_set(self.songs.all(), 'features')


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    songs = models.ManyToManyField('music.Song', blank=True, on_delete=models.SET_DEFAULT, related_name='on_playlists')
    artwork = models.ImageField(verbose_name='Playlist Artwork')
    duration = models.DurationField(default=0)
    created = models.DateTimeField(default=timezone.now)
    last_edited = models.DateTimeField(default=timezone.now, verbose_name='Last Edited')

    def __str__(self):
        return self.title

    @property
    def artists(self):
        return get_property_set(self.songs.all(), 'artists')

    @property
    def features(self):
        return get_property_set(self.songs.all(), 'features')

    @property
    def albums(self):
        return get_property_set(self.songs.all(), 'album')


class Song(models.Model):
    title = models.CharField(max_length=200)
    artists = models.ManyToManyField('music.Artist', blank=True, verbose_name='Artist(s)', related_name='songs')
    features = models.ManyToManyField('music.Artist', blank=True, verbose_name='Feature(s)', related_name='featured_on')
    album = models.ForeignKey('music.Album', blank=True, on_delete=models.SET_DEFAULT, related_name='songs')
    duration = models.DurationField(default=0)
    released = models.DateField(blank=True)

    def __str__(self):
        return self.title
