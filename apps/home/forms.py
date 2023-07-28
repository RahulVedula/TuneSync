from django import forms

class SpotifyForm(forms.Form):
    playlistName = forms.CharField(max_length=100)
    creator = forms.CharField(max_length=100)
    SpotifyURI = forms.CharField(max_length=100)

class YoutubeForm(forms.Form):
    playlistName = forms.CharField(max_length=100)
    creator = forms.CharField(max_length=100)
    youtubeLink = forms.CharField(max_length=100)

class newPlaylistForm(forms.Form):
    playlistName = forms.CharField(max_length=100)
    creator = forms.CharField(max_length=100)
    SpotifyURI = forms.CharField(max_length=100)

class SearchForm(forms.Form):
    search_query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search...'}))