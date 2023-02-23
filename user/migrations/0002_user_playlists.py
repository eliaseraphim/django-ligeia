# Generated by Django 4.1.7 on 2023-02-23 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_playlist_created_by'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='playlists',
            field=models.ManyToManyField(blank=True, related_name='+', to='music.playlist'),
        ),
    ]
