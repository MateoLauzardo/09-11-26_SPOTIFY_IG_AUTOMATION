import os
import time
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth



load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI", "http://127.0.0.1:8888/callback")


# read-only scopes: what's playing now + which device / shuffle / volume state
SCOPE = "user-read-currently-playing user-read-playback-state"


#NOTE Logins into my spotify
def get_client():
    """Log in (opens a browser the first time) and cache the token in .cache."""
    auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=SCOPE,
        cache_path=".cache",
        open_browser=True,
    )
    return spotipy.Spotify(auth_manager=auth)


#NOTE this just formats milliseconds its, minutes and seconds
def fmt_ms(ms):
    seconds = ms // 1000
    return f"{seconds // 60}:{seconds % 60:02d}"


#NOTE This just returns a summary of the song playying (requires the playback object from the spotify api)
def describe(playback):
    """Turn a currently-playing payload into a one-line summary, or None if idle."""
    if not playback or not playback.get("item"):
        return None

    item = playback["item"]
    artists = ", ".join(a["name"] for a in item.get("artists", []))
    position = fmt_ms(playback.get("progress_ms") or 0)
    duration = fmt_ms(item.get("duration_ms") or 0)
    state = "▶" if playback.get("is_playing") else "❚❚"

    return f"{state} {item['name']} — {artists}  [{position}/{duration}]"



#TODO - Implement the function to share the currently playing song with me on Instagram
# def share_with_me_IG():




def main():
    
    if not client_id or not client_secret:
        raise SystemExit("Set CLIENT_ID and CLIENT_SECRET in .env")

    sp = get_client()
    me = sp.me()
    
    print(f"Logged in as {me['display_name']} ({me['id']})\n")

    last = None
    
    while True:
        playback = sp.current_playback() 
        line = describe(playback)

        if line is None:
            if last != "idle":
                print("Nothing playing right now.")
                last = "idle"
        else:
            track_id = (playback["item"] or {}).get("id")
            if track_id != last:
                print(line)
                last = track_id

        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
