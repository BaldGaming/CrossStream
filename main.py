import time
import random
from spotify_client import get_liked_songs, get_spotify_uri, create_playlist_and_add
from ytm_client import (
    get_video_id,
    create_ytm_playlist,
    add_to_ytm_playlist,
    get_playlist_tracks,
)

# Notify the user
print("--- Welcome to CrossStream! ---")
print("This program will sync your playlists across Spotify and YouTube Music.\n")

# Prompt the user
choice = input("Type 1 to move Spotify -> YTM, or 2 to move YTM -> Spotify: ")

# Spotify to YouTube Music
if choice == "1":

    # Return a list of liked songs and update the exported amount
    ret_list = get_liked_songs()
    print(
        f"Successfully fetched {len(ret_list)} songs from your Spotify Liked library."
    )

    # Prompt the user to enter a title
    name = input("Enter a name for your new YouTube Music playlist: ")
    ytm_playlist_id = create_ytm_playlist(name)
    print(f"Created/Using playlist ID: {ytm_playlist_id}")

    found_video_ids = []
    imported_count = 0

    print("\nStarting search... this may take a while.\n")

    start_time = time.time()  # Capture the start time

    # We loop through the entire list of ids
    for song in ret_list:
        print(f"Searching for: {song['track']} by {song['artist']}...")

        # We pass the song's artist and track name
        video_id = get_video_id(song["artist"], song["track"])

        if video_id:
            found_video_ids.append(video_id)
            imported_count += 1
            print(f"Found! (Total found: {imported_count})")
        else:
            print("Could not find this track on YouTube Music.")

        # Force the script to wait a second per batch so that we don't get ip banned xd
        sleep_time = random.uniform(0.2, 0.6)
        time.sleep(sleep_time)

    print(f"\nFinalizing... uploading {len(found_video_ids)} tracks to YouTube Music.")
    # We pass the playlist id and the list into add_to_ytm_playlist()
    add_to_ytm_playlist(ytm_playlist_id, found_video_ids)

    # Calculate duration
    end_time = time.time()
    total_time = end_time - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)

    print(f"\nDone! Process completed in {minutes}m {seconds}s.")

# YouTube Music to Spotify
elif choice == "2":
    # Prompt the user for the Playlist ID
    ytm_playlist_id = input("Paste the YouTube Music Playlist ID: ")

    # Return a list of songs from the YTM playlist
    ytm_list = get_playlist_tracks(ytm_playlist_id)
    print(f"Successfully fetched {len(ytm_list)} songs from YouTube Music.\n")

    # Prompt the user for a name
    name = input("Enter a name for your new Spotify playlist: ")

    found_spotify_uris = []
    imported_count = 0

    print("\nStarting search... this may take a while.\n")

    start_time = time.time()  # Capture the start time

    # The Loop
    for song in ytm_list:
        print(f"Searching for: {song['track']} by {song['artist']}...")

        # We pass the song's artist and track name
        uri = get_spotify_uri(song["artist"], song["track"])

        if uri:
            found_spotify_uris.append(uri)
            imported_count += 1
            print(f"Found! (Total found: {imported_count})")
        else:
            print("Could not find this track on Spotify.")

        # Force the script to wait a second per batch so that we don't get ip banned xd
        sleep_time = random.uniform(0.2, 0.6)
        time.sleep(sleep_time)

    print(f"\nFinalizing... creating playlist '{name}' on Spotify.")
    # We pass the name and the list into create_playlist_and_add()
    create_playlist_and_add(name, found_spotify_uris)

    # Calculate duration
    end_time = time.time()
    total_time = end_time - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)

    print(f"\nDone! Process completed in {minutes}m {seconds}s.")
