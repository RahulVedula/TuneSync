# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Playlist
from .models import Song

# Register your models here.

admin.site.register(Playlist)
admin.site.register(Song)