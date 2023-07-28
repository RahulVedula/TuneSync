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


def find_track_and_add_to_playlist(title, playlist_id):
    sp = spotipy.Spotify(auth = spotify_token)
    results = sp.search(q=title, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id, [track_uri])


def find_track(title):
    sp = spotipy.Spotify(auth = spotify_token)
    results = sp.search(q=title, type='track', limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['uri']
    else:
        return None

def get_song_details(track_name):
    sp = spotipy.Spotify(auth = spotify_token)
    track_uri = find_track(track_name)
    if track_uri:
        track_info = sp.track(track_uri)
        image_url = track_info['album']['images'][0]['url']
        title = track_info['name']
        duration = track_info['duration_ms']//1000
        artist = track_info['artists'][0]['name']
        album_name = track_info['album']['name']
        added_at = datetime.now().strftime('%Y-%m-%d') 
        external_urls = track_info['external_urls']
        spotify_link = external_urls.get('spotify', None)

        return {
            'image_url': image_url,
            'title': title,
            'duration': duration,
            'artist': artist,
            'album_name': album_name,
            'added_date': added_at,
            'spotify_link': spotify_link,

        }
    else:
        return None

CLIENT_SECRETS_PATH = Path(__file__).parent / 'client_secrets.json'

# Initialize the YouTube Data API
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_PATH, ['https://www.googleapis.com/auth/youtube'])
    credentials = flow.run_local_server()

    return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

def get_video_id(service, song_name):
    search_response = service.search().list(
        q=song_name,
        part='id',
        maxResults=1,
        type='video'
    ).execute()

    if 'items' in search_response:
        video_id = search_response['items'][0]['id']['videoId']
        return video_id
    else:
        return None

def add_to_playlist(service, playlist_link, video_id):
    playlist_id = playlist_link.split('list=')[1]

    try:
        service.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        ).execute()
        return True
    except googleapiclient.errors.HttpError as e:
        print(f"Error: {e}")
        return False