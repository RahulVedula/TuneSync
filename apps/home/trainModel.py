import pandas as pd
from .secrets import spotify_token
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

data = {
    'song_name': ['Song A', 'Song B', 'Song C', 'Song D', 'Song E'],
    'features': [
        'upbeat catchy pop',
        'mellow acoustic folk',
        'energetic rock',
        'romantic ballad',
        'upbeat catchy pop rock'
    ]
}

df = pd.DataFrame(data)

def recommend_songs(input_song, df, num_recommendations=5):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['features'])
    input_song_index = df[df['song_name'] == input_song].index[0]
    cosine_similarities = linear_kernel(tfidf_matrix[input_song_index], tfidf_matrix)
    similar_song_indices = cosine_similarities[0].argsort()[::-1][1:num_recommendations+1]
    recommended_songs = df.loc[similar_song_indices, 'song_name'].values

    return recommended_songs
  
def get_spotify_recommendations(track_name, num_recommendations=5):
    sp = spotipy.Spotify(auth=spotify_token)
    results = sp.search(q=track_name, type='track', limit=1)

    if not results['tracks']['items']:
        return []

    track_id = results['tracks']['items'][0]['id']
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=num_recommendations)
    recommended_tracks = [track['name'] for track in recommendations['tracks']]

    return recommended_tracks
def get_spotify_data(query, num_results=10):
    sp = spotipy.Spotify(auth=secret_token)
    results = sp.search(q=query, type='track', limit=num_results)
    song_names = []
    artists = []
    albums = []
    genres = []
    release_years = []
    popularity = []
    features = []

    for track in results['tracks']['items']:
        song_names.append(track['name'])
        artists.append(track['artists'][0]['name'])
        albums.append(track['album']['name'])
        genres.append(track['artists'][0]['genre'])  
        release_years.append(int(track['album']['release_date'][:4]))
        popularity.append(track['popularity'])
        audio_features = sp.audio_features(track['id'])[0]
        features.append([audio_features['danceability'], audio_features['energy'], 
                         audio_features['loudness'], audio_features['acousticness'], 
                         audio_features['instrumentalness']])

    data = {
        'song_name': song_names,
        'artist': artists,
        'album': albums,
        'genre': genres,
        'release_year': release_years,
        'popularity': popularity,
        'features': features
    }

    df = pd.DataFrame(data)
    return df
