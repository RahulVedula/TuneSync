# TuneSync
TuneSync is a media platform enabling cross-platform connections for playlists. TuneSync uses a combination of Django, REST Frameworks, and React.js paired with Youtube v3 and Spotify API to provide a user-friendly interface -- simply open the site, login, and enjoy free, unlimited sharing or discovery for any type of playlists(Youtube, Spotify, or make your own). 

Users can choose one of three options when making new playlists, this option will use import existing spotify playlists and make a new youtube playlist, linking the two playlists for future sharing or editing:
![Screen Shot 2023-07-29 at 1 08 25 AM](https://github.com/RahulVedula/TuneSync/assets/107275556/3cce5e8e-182f-42fa-afe1-35dd4c63a31d)

Users are also given the option to discover new playlists that are publicized by users:
![Screen Shot 2023-07-29 at 1 08 33 AM](https://github.com/RahulVedula/TuneSync/assets/107275556/4d07a2f2-f16e-41f9-85cb-fffe892bef39)


Users can view their playlists and choose to delete or add songs (which will automatically add/delete it to the spotify/youtube playlist):
![Screen Shot 2023-07-29 at 1 07 45 AM](https://github.com/RahulVedula/TuneSync/assets/107275556/91805067-5c54-4268-936f-df64ebe518af)

Users are also free to add songs to their playlist, with an established autocomplete function: 
![Screen Shot 2023-07-29 at 1 07 59 AM](https://github.com/RahulVedula/TuneSync/assets/107275556/1749fb28-4d9a-41ce-a4d9-4ea11d393d77)

To see other features like Youtube Imports, customized playlists, or recommended songs, please clone the site or visit the deployed version. If cloning the cite, please make sure to download the following modules:
 - spotipy
 - google-api-python-client
 - requests
 - datetime
 - pandas
 - sys
 - pathlib
 - beautifulsoup4
 - pyquery
 - django (Please ensure all are stored in a virtual environment with the correct app names/directories and collected static files)
