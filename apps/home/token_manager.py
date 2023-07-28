import requests
import time

class SpotifyTokenManager:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.token_expiration_time = 0

    def get_access_token(self):
        # Check if the current access token is valid (not expired)
        if self.access_token and self.token_expiration_time > time.time():
            return self.access_token

        # If the access token is expired or not available, refresh it
        self.access_token = self.refresh_access_token()
        return self.access_token

    def refresh_access_token(self):
        # Spotify Accounts service URL for obtaining a new access token
        token_url = 'https://accounts.spotify.com/api/token'

        # Set the data to send in the POST request
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            # Send the POST request to the token URL with the data
            response = requests.post(token_url, data=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the new access token from the response
                access_token = response.json()['access_token']
                # Set the expiration time for the new access token (usually 1 hour from now)
                self.token_expiration_time = time.time() + 3600
                return access_token
            else:
                print("Failed to refresh access token. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("Error refreshing access token:", e)
            return None
