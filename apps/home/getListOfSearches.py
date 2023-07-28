import os
import requests
import argparse
from .secrets import spotify_token
import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from .models import Song, Playlist
import re


def get_all_tracks(playlist_id,playlist):
    sp = spotipy.Spotify(auth=spotify_token)
    results = []
    songList = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.playlist_tracks(playlist_id, limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            results += [val]
            image_url = track['album']['images'][0]['url'] 
            spotify_url = track['external_urls']['spotify']
            album = track['album']['name']
            duration =  track['duration_ms']//1000 
            added_at = datetime.now().strftime('%Y-%m-%d') 
            song, created = Song.objects.get_or_create(title=track['name'], writer=track['artists'][0]['name'],  image_url=image_url, link=spotify_url, duration=duration,album_name=album,added_date=added_at)
            playlist.songs.add(song.id)
        if (len(curGroup) < 50):
            break
    playlist.songs.add(*songList)
    playlist.save()
    return results

def get_spotify_link_from_uri(spotify_uri):
    # Initialize the Spotify API client
    sp = spotipy.Spotify(auth=spotify_token)

    uri_pattern = r'(?<=:)([a-zA-Z0-9]+)$'
    match = re.search(uri_pattern, spotify_uri)

    if not match:
        print("Invalid Spotify URI.")
        return None

    spotify_id = match.group(1)

    try:
        if "playlist" in spotify_uri:
            playlist = sp.playlist(spotify_id)
            spotify_link = playlist['external_urls']['spotify']
        else:
            track = sp.track(spotify_id)
            spotify_link = track['external_urls']['spotify']
        return spotify_link
    except Exception as e:
        print(f"Error occurred while fetching details: {e}")
        return None
    
def get_playlist_image(spotify_uri):
    sp = spotipy.Spotify(auth=spotify_token)
    results = sp.playlist(spotify_uri)
    playlist_cover_url = results['images'][0]['url']
    return playlist_cover_url
