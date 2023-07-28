from .token_manager import SpotifyTokenManager

client_id = '06dc2eb821914453b2442f81016a9086'
client_secret = '3871bca8621e4c1ba5d6d5b684281f86'
refresh_token = 'AQCSXR5Re71Cvn-z8Y4umArtCp-5BgttJp2l7K_dhApW3hH9gHyd4fNNh2ZOylHmK-IJjbPkczCat9UEQZ-axhv4jjLRpeY2QJjXCUYHqmTFhMUFnB7dE5hyaMCo4Tp2bHM'

token_manager = SpotifyTokenManager(client_id, client_secret, refresh_token)

# Now, whenever you need an access token, use the token manager to get it
spotify_token = token_manager.get_access_token()