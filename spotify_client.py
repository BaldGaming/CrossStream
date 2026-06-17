import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

# Extract "secrets"
with open("secrets.json", "r") as file:
    secrets = json.load(file)

CLIENT_ID = secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = secrets["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-library-read playlist-modify-private"

# Initialize Spotipy
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )
)


# This function extracts data from the liked songs playlist into a big list.
def get_liked_songs():
    print("\nFetching your liked songs from Spotify...")

    # A list to store clean data
    my_songs = []

    # Set the starting point
    current_offset = 0

    # An infinite loop that draws 50 songs per batch
    while True:

        # Ask Spotify for 50 songs, starting at your current_offset
        results = sp.current_user_saved_tracks(limit=50, offset=current_offset)

        # Extract the actual list of items from the Spotify response
        items = results["items"]

        # Break if we've reached the end of the playlist
        if len(items) == 0:
            break

        # Loop through the 50 songs we just grabbed
        for item in items:
            # The data we need is buried in a dictionary.
            track_name = item["track"]["name"]
            artist_name = item["track"]["artists"][0]["name"]

            # Create a clean dictionary for this song
            song_data = {"artist": artist_name, "track": track_name}

            # Append it to our list
            my_songs.append(song_data)

        # Notify user which song was fetched and how many are left
        print(f"Fetched {len(my_songs)} songs so far...")

        # Add 50 to the offset to turn the page for the next loop
        current_offset += 50

    # Reports to the user
    print(f"\nFinished! Total liked songs extracted: {len(my_songs)}")

    # Return the final list
    return my_songs


# This function fetches the "URI" for each song
def get_spotify_uri(artist, song_name):

    # Set the specific format which we will use to search for songs
    search_query = f"track:{song_name} artist:{artist}"

    # We pass our formatted string into 'q' (query).
    # 'type' tells Spotify we only want tracks
    # 'limit=1' tells Spotify to only give us the single best match.
    results = sp.search(q=search_query, type="track", limit=1)

    # We navigate down the JSON path to isolate the list of items
    items_list = results["tracks"]["items"]

    # Check to make sure the search didn't return an empty list
    if len(items_list) > 0:

        # Grab the very first item from the list, and extract its 'uri'
        track_uri = items_list[0]["uri"]

        return track_uri

    else:
        # If the search failed, return None
        return None


# This function creates a new playlist and adds track URIs to it
def create_playlist_and_add(playlist_name, track_uris):

    # Grab the current user's id
    user_info = sp.current_user()
    user_id = user_info["id"]
    display_name = user_info.get("display_name", "User")
    print(f"Fetched {display_name}'s id: {user_id}")  # Notify the user

    # Create a new playlist for this specific user,
    # and prompt the user to give the playlist a name
    new_playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description="Created using CrossStream App",
    )

    print(f"Playlist created successfully! id: {new_playlist['id']}")  # Notify the user

    # We add the songs to the playlist in chunks of 100 songs per batch
    try:
        for i in range(0, len(track_uris), 100):  # 100 songs chunks
            chunk = track_uris[i : i + 100]
            sp.playlist_add_items(new_playlist["id"], chunk)
            print(f"{len(chunk)} URIs we're successfully added!")  # Notify the user

    except Exception as e:
        print(f"An error occurred: {e}")
