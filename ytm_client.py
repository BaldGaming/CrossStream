import time
from ytmusicapi import YTMusic, OAuthCredentials

ytm = YTMusic("browser.json")


# This function searches YouTube Music for a song and returns it's unique videoId.
def get_video_id(artist, song_name):

    # Combine the artist and song into a single search string.
    search_query = f"{artist} {song_name}"

    # Pass the argument filter="songs" so it doesn't return music videos or fan covers
    results = ytm.search(query=search_query, filter="songs")

    if len(results) > 0:
        return results[0]["videoId"]
    else:
        return None


# This function creates an empty YTM playlist and returns its id
def create_ytm_playlist(playlist_name):

    print(f"Creating YouTube Music playlist: '{playlist_name}'...")

    # Create the playlist and save the returned ID
    return ytm.create_playlist(
        title=playlist_name, public=True, description="Created using CrossStream App"
    )


# This function takes a YTM playlist id and a list of video ids, then adds them all at once
def add_to_ytm_playlist(playlist_id, song_ids):
    chunk_size = 20  # Smaller chunks are much more reliable
    for i in range(0, len(song_ids), chunk_size):
        chunk = song_ids[i : i + chunk_size]
        try:
            # We add a 2-second delay between batches to avoid the "400 Bad Request" rate limit
            time.sleep(2)
            ytm.add_playlist_items(playlistId=playlist_id, videoIds=chunk)
            print(f"Added batch starting at index {i} ({len(chunk)} songs).")
        except Exception as e:
            print(f"Error adding batch at index {i}: {e}")

    print(f"Completed processing {len(song_ids)} songs.")


# Takes a YTM playlist id, extracts all of the songs then returns a clean list
def get_playlist_tracks(playlist_id):

    print("Fetching tracks from YouTube Music playlist...")

    playlist_data = ytm.get_playlist(playlistId=playlist_id)
    tracks = playlist_data["tracks"]

    my_ytm_songs = []

    # Loop through the data dictionary to extract the data we need
    for item in tracks:
        try:
            title = item["title"]
            artist = item["artists"][0]["name"]

            my_ytm_songs.append({"artist": artist, "track": title})
        except Exception:
            continue

    print(f"Fetched {len(my_ytm_songs)} songs from YouTube Music!")
    return my_ytm_songs
