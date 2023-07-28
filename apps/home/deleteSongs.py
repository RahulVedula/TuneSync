import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from .secrets import spotify_token
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from pathlib import Path
import googleapiclient.errors
from google.auth.transport.requests import Request

def delete_track_by_name(playlist_id, track_name):
    sp = spotipy.Spotify(auth=spotify_token)

    # Search for the track by name
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']

        # Remove the track from the playlist
        try:
            sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=[track_uri])
            print(f"Track '{track_name}' removed from playlist successfully!")
        except spotipy.exceptions.SpotifyException as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Track '{track_name}' not found in Spotify.")