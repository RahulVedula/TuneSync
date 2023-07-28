# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("playlist/", views.playlist, name='playlist'),
    path("form_handle/", views.form_handle, name='form_handle'),
    path("youtube_playlist/", views.youtube_playlist, name='youtube_playlist'),
    path("playlists/",views.visitUserPlaylist,name = 'playlists'),
    path("discover/",views.discoverPlaylist,name = 'discover'),
    path('playlist/<str:playlist_name>/', views.specificPlaylist, name='playlist_detail'),
    path('delete_song/<str:playlist_name>/<int:song_pk>/', views.delete_song_view, name='delete_song'),
    path('playlist/<str:playlist_name>/search/', views.search_view, name='search'),
    path('get_related_searches/', views.get_related_searches, name='get_related_searches'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
