# CrossStream 🎧

A Python-based synchronization engine that bridges your music libraries across Spotify and YouTube Music. 

CrossStream extracts your tracks from one platform, searches for the exact matches on the other, and safely batches them into a new playlist while respecting API rate limits.

## Features
* **Bi-directional Syncing:** Move your "Liked Songs" from Spotify to YouTube Music, or transfer any YouTube Music playlist to Spotify.
* **Intelligent Batching:** Automatically splits large playlists into chunks and throttles requests to bypass strict Google/Spotify API rate limits and `400 Bad Request` errors.
* **Interactive CLI:** Simple text prompts guide you through selecting your sync direction and naming your new playlists.

## Prerequisites
* Python 3.x
* A Spotify Developer account (to get API credentials)
* A YouTube Music account

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/CrossStream.git](https://github.com/yourusername/CrossStream.git)
cd CrossStream
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration & Authentication

Before running the script, you need to authenticate with both platforms. **Never share or commit these configuration files to GitHub.**

### 1. Spotify Authentication (`secrets.json`)
Create a file named `secrets.json` in the root directory of the project. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/), create an app, set the Redirect URI to `http://127.0.0.1:8888/callback`, and paste your credentials:

```json
{
    "SPOTIFY_CLIENT_ID": "your_client_id_here",
    "SPOTIFY_CLIENT_SECRET": "your_client_secret_here"
}
```

### 2. YouTube Music Authentication (`browser.json`)
This project uses `ytmusicapi` which requires authenticated browser headers.
1. Open your terminal in the project folder and run:
```bash
ytmusicapi browser
```
2. Open YouTube Music in your browser, open the Network tab (F12), and copy the Request Headers from a `browse` request.
3. Paste the `authorization`, `cookie`, `x-goog-visitor-id`, `x-goog-authuser`, and `user-agent` headers into the terminal and press `Enter`, `Ctrl+Z`, `Enter`.
4. This will generate a `browser.json` file in your directory.

## Usage

Run the main script to launch the interactive prompt:

```bash
python main.py
```

Follow the on-screen instructions to select your sync direction and name your playlists. Grab a coffee—large libraries may take a few minutes as the script deliberately throttles search requests to prevent temporary API bans!
