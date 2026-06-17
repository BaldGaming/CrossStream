import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# 1. Open the JSON file and read it
with open("secrets.json", "r") as file:
    secrets = json.load(file)

# 2. Extract your keys into variables
CLIENT_ID = secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = secrets["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8888/callback"

# Initialize the Spotipy client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read",
    )
)

def get_liked_songs():
    while