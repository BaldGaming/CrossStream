from ytmusicapi import YTMusic

try:
    # This will load "browser.json" automatically if it's in the same folder
    ytm = YTMusic("browser.json")
    print("SUCCESS: Library loaded! Attempting to fetch library...")
    ytm.get_library_songs(limit=1)
    print("SUCCESS: Credentials are valid.")
except Exception as e:
    print(f"FAILED: {e}")