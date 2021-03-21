import spotipy
from spotipy.oauth2 import SpotifyOAuth
import uuid

# Simple wrapper methods for authentication

def get_spotify_oauth(scope, client_id, client_secret, redirect_uri, cache_handler=spotipy.cache_handler.CacheFileHandler):
    return SpotifyOAuth(
        scope=scope, 
        client_id=client_id, 
        client_secret=client_secret, 
        redirect_uri=redirect_uri, 
        cache_handler=cache_handler)

def authenticate_user_get_url(spotify_oauth):
    return spotify_oauth.get_authorize_url()

def authenticate_user_get_token(spotify_oauth, url):
    code = spotify_oauth.parse_response_code(url)
    if code != url:
        token = spotify_oauth.get_access_token(code)
        return token
    else:
        raise Exception("The URL is invalid or does not contain a valid response code.")
