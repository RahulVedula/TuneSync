# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SpotifyForm, SearchForm,YoutubeForm
from .models import Playlist, Song
from .getListOfSearches import get_all_tracks, get_playlist_image, get_spotify_link_from_uri
from .spotifyToYoutube import create_youtube_playlist,add_songs_to_youtube_playlist,get_credentials
from googleapiclient.discovery import build
from .searchSongs import get_track_details
from .addSongs import get_authenticated_service,get_song_details,get_video_id,find_track_and_add_to_playlist,add_to_playlist
import requests
from .deleteSongs import delete_track_by_name
from .youtubeToSpotify import extract_titles,find_track_and_add_to_playlist,create_playlist




@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required
def playlist(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('playlist/playlistMaker.html')
    return HttpResponse(html_template.render(context, request))

@login_required
def visitUserPlaylist(request):
    playlists = Playlist.objects.filter(user=request.user)    
    html_template = loader.get_template('playlist/userPlaylists.html')
    return HttpResponse(html_template.render({'playlists': playlists}, request))

def discoverPlaylist(request):
    playlists = Playlist.objects.all()
    html_template = loader.get_template('playlist/discover.html')
    return HttpResponse(html_template.render({'playlists': playlists}, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def form_handle(request):
    form = SpotifyForm()
    if request.method == 'POST':
        form = SpotifyForm(request.POST)
        try:
            if form.is_valid():
                cd = form.cleaned_data
                spotifyURI = cd.get('SpotifyURI')
                print(f"The value of spotify: {spotifyURI}")  
                playlist_name = cd.get("playlistName")
                count = 1
                while Playlist.objects.filter(name=playlist_name).exists():
                    playlist_name = f"{cd.get('playlistName')} {count}"
                    count += 1
                playlist_instance = Playlist.objects.create(name = cd.get("playlistName"),creator = cd.get('creator'),spotifyURI=spotifyURI)
                song_titles = get_all_tracks(spotifyURI,playlist_instance)
                creds = get_credentials()
                youtube = build('youtube', 'v3', credentials=creds)
                youtubeURL,youtube_playlist_id = create_youtube_playlist(youtube, cd.get("playlistName"), song_titles)
                add_songs_to_youtube_playlist(youtube, youtube_playlist_id, song_titles)
                playlist_instance.save()
                playlist_instance.youtubeLink = youtubeURL
                playlist_instance.save()
                playlist_instance.image_url = get_playlist_image(spotifyURI)
                playlist_instance.save()
                playlist_instance.spotifyLink = get_spotify_link_from_uri(spotifyURI)
                playlist_instance.save()
        except Exception as e:
            print("Error occurred during form submission:", e)
    html_template = loader.get_template('playlist/playlistMaker.html')
    return HttpResponse(html_template.render({'form': form}, request))

def youtube_playlist(request):
    form = YoutubeForm()
    if request.method == 'POST':
        form = YoutubeForm(request.POST)
        try:
            if form.is_valid():
                cd = form.cleaned_data
                youtubeURL = cd.get('youtubeLink')
                playlist_name = cd.get("playlistName")
                count = 1
                while Playlist.objects.filter(name=playlist_name).exists():
                    playlist_name = f"{cd.get('playlistName')} {count}"
                    count += 1
                playlist_instance = Playlist.objects.create(name = cd.get("playlistName"),creator = cd.get('creator'),youtubeLink=youtubeURL, user = request.user,)
                search_result = requests.get(youtubeURL).text
                titles = extract_titles(search_result)
                song_titles = titles[:-8]
                spotifyURI = create_playlist(playlist_name)
                playlist_instance.spotifyURI = get_spotify_link_from_uri(spotifyURI)
                playlist_instance.save()
                playlist_instance.spotifyLink = get_spotify_link_from_uri(spotifyURI)
                playlist_instance.save()
                for i in range(len(song_titles)):
                    find_track_and_add_to_playlist(song_titles[i],spotifyURI)
                    information = get_song_details (song_titles[i])
                    song, created = Song.objects.get_or_create(title=information['title'], writer=information['artist'],  image_url=information['image_url'], link=information['spotify_link'], duration=information['duration'],album_name=information['album_name'],added_date=information['added_date'])
                    playlist_instance.songs.add(song.id)
                print("reached")
                playlist_instance.image_url = get_playlist_image(spotifyURI)
                playlist_instance.save()
                
        except Exception as e:
            print("Error occurred during form submission:", e)
    html_template = loader.get_template('playlist/youtubePlaylistMaker.html')
    return HttpResponse(html_template.render({'form': form}, request))

def specificPlaylist(request,playlist_name):
        playlist_instance = get_object_or_404(Playlist, name=playlist_name)
        html_template = loader.get_template('playlist/specificPlaylist.html')
        return HttpResponse(html_template.render({'playlist': playlist_instance}, request))

def delete_song_view(request,playlist_name, song_pk):
    # Retrieve the song instance based on the primary key
    playlist = Playlist.objects.get(name=playlist_name)
    song = get_object_or_404(Song, pk=song_pk)
    delete_track_by_name(playlist.spotifyURI,song.title)
    song.delete()

    # Redirect the user to a new page after successful deletion
    return redirect(request.META.get('HTTP_REFERER', '/'))

def search_view(request, playlist_name):
    playlist = Playlist.objects.get(name=playlist_name)
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            related_search_results = get_track_details(search_query)
            print("Received search query:", search_query)
            playlist = Playlist.objects.get(name=playlist_name)
            information = get_song_details (search_query)
            song, created = Song.objects.get_or_create(title=information['title'], writer=information['artist'],  image_url=information['image_url'], link=information['spotify_link'], duration=information['duration'],album_name=information['album_name'],added_date=information['added_date'])
            playlist.songs.add(song.id)
            find_track_and_add_to_playlist(search_query,playlist.spotifyURI)
            try:
                service = get_authenticated_service()
                video_id = get_video_id(service, search_query)

                if video_id:
                    if add_to_playlist(service, playlist.youtubeLink, video_id):
                        print("Song added to the playlist!")
                    else:
                        print("Failed to add the song to the playlist.")
                else:
                    print(f"Song '{search_query}' not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
            return redirect('playlist_detail', playlist_name=playlist_name)

    else:
        form = SearchForm()

    return render(request, 'playlist/search.html', {'form': form, 'playlist': playlist})


def get_related_searches(request):
    search_query = request.GET.get('q')
    print(search_query)
    related_search_results = get_track_details(search_query)
    return render(request, 'playlist/related_search_results.html', {'related_search_results': related_search_results})
