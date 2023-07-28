from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import requests
import re
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from .getListOfSearches import get_all_tracks

def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    
    # Get the absolute path to the client_secrets.json file
    secrets_file_path = Path(__file__).parent / 'client_secrets.json'

    # Prompt the user to authorize the application
    flow = InstalledAppFlow.from_client_secrets_file(secrets_file_path, SCOPES)
    creds = flow.run_local_server(port=0)

    return creds

def create_youtube_playlist(youtube, playlist_title, song_titles):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": "My new playlist created with the YouTube API.",
                "tags": ["sample playlist", "youtube api"],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    playlist_id = response['id']
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

    return playlist_url, playlist_id

def add_songs_to_youtube_playlist(youtube, playlist_id, song_titles):
    for song_title in song_titles:
        try:
            video_id = ScrapeVidId(song_title)
            if video_id:
                request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                )
                request.execute()
                print(f"Added {song_title} to the playlist.")
            else:
                print(f"Couldn't find a video for {song_title}. Skipping.")
        except Exception as e:
            print(f"Error adding {song_title} to the playlist:", e)

def ScrapeVidId(search):
    words = search.split()
    search_link = "https://www.youtube.com/results?search_query=" + '+'.join(words)
    search_result = requests.get(search_link).text
    # Parse the HTML using BeautifulSoup
    pattern = r'"watchEndpoint":{"videoId":"(.*?)",'
    match = re.search(pattern, search_result)

    if match:
        video_id = match.group(1)
        print("Video ID:", video_id)
        return video_id
    else:
        print("Video ID not found in the HTML snippet.")
        return None

