from django.db import models
from django.contrib.auth.models import User

def get_default_user_id():
    default_user, _ = User.objects.get_or_create(username='rahul')
    return default_user.id

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user_id)
    name = models.CharField(max_length=100, default="")
    image_url = models.URLField(default="https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2")  # Add the image URL field
    creator = models.CharField(max_length=100, default="Unknown")
    songs = models.ManyToManyField('Song')
    spotifyURI = models.CharField(max_length=100, default="")
    spotifyLink = models.URLField(default="")
    youtubeLink = models.URLField(default="")

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=100, default="")
    writer = models.CharField(max_length=100, default="")
    link = models.URLField()
    image_url = models.URLField(default="https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2")  
    duration = models.PositiveIntegerField(default=0)  # Duration in seconds
    added_date = models.DateField(null=True, blank=True)  # Date the song was added to the playlist
    album_name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title
    def get_duration_display (self):
        minutes, seconds = divmod(self.duration, 60)
        return f"{minutes:02d}:{seconds:02d}"
