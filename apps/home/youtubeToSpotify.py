from .secrets import spotify_token
import spotipy
import json
import requests
from bs4 import BeautifulSoup
import re

def extract_titles(html_data):
    # Parse the HTML content
    soup = BeautifulSoup(html_data, 'lxml')

    # Search for all the patterns in the HTML using a regular expression
    pattern = r'"title":{"runs"\:\[{"text":"([^"]+)"'
    matches = re.finditer(pattern, str(soup))

    titles = []
    for match in matches:
        # Extract the title from each matched pattern
        title = match.group(1)
        titles.append(title)

    return titles

def create_playlist(playlist_name):
    sp = spotipy.Spotify(auth=spotify_token)
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name)
    playlist_uri = playlist['uri']
    return playlist_uri

def find_track_and_add_to_playlist(title, playlist_id):
    sp = spotipy.Spotify(auth = spotify_token)
    results = sp.search(q=title, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id, [track_uri])

