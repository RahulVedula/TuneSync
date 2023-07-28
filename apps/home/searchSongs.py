from spotipy.oauth2 import SpotifyClientCredentials
from .secrets import spotify_token
import spotipy
import sys

def get_track_details(search_str):
    sp = spotipy.Spotify(auth=spotify_token)
    result = sp.search(search_str)

    track_details = []

    # Limit the results to the first 10 tracks
    for track in result['tracks']['items'][:10]:
        track_name = track['name']
        cover_url = track['album']['images'][0]['url']  # Get the URL of the first image (cover)
        artist_names = ", ".join([artist['name'] for artist in track['artists']])
        
        track_details.append((track_name, artist_names, cover_url))
    
    return track_details