import os
import time
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from conversion import fmt_ms  # Import the fmt_ms function from conversion.py


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI", "http://127.0.0.1:8888/callback")

# read-only scopes: what's playing now + which device / shuffle / volume state
SCOPE = "user-read-currently-playing user-read-playback-state"




#Logins into my spotify
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



"""
    Describe the current playback state.

    playback = {
        "is_playing": True,
        "progress_ms": 123385,          # 2:03 into the song
        "item": {                       # ← the track, its own dict
            "name": "Heads Will Roll",
            "id": "18oWEPapjNt32E6sCM6VLb",
            "duration_ms": 221000,      # 3:41 long
            "artists": [                # ← a LIST of dicts
                {"name": "Yeah Yeah Yeahs", "id": "3TNt..."}
            ]
        },
        "device": {...}, "shuffle_state": ..., "repeat_state": ...
        }

"""


#This just returns the song playing, artist name, position and duration 
def describe(playback):



    if not playback or not playback.get("item"):
        return None

    item = playback["item"] # dictionary of the song playing right now


    artists = ""

    # .get gives you the item in the dictionary, if it exists, otherwise it returns None. This is safer than using item["artists"] directly, which would raise a KeyError if "artists" is not present in the dictionary.
    for a in item.get("artists", []):

        if artists:
            artists += ", "

        artists += a["name"]
        


    position = fmt_ms(playback.get("progress_ms"))
    duration = fmt_ms(item.get("duration_ms"))
    state = "▶" if playback.get("is_playing") else "❚❚"

    return f"{state} {item['name']} — {artists}  [{position}/{duration}]"




# connecting everything together will be plugged into main 
def spotify_logic():
    
    if not client_id or not client_secret:
        raise SystemExit("Set CLIENT_ID and CLIENT_SECRET in .env")

    sp = get_client()
    me = sp.me() # gets a hashmap of name and id 
    
    print(f"Logged in as {me['display_name']} ({me['id']})\n")






    # flag
    last = None
    
    
    while True:
        
        playback = sp.current_playback() 
        line = describe(playback) 
        
        
        # detecets if nothing is playing right now
        if line is None:
            if last != "idle":
                print("Nothing playing right now.")
                last = "idle"
        
        
        
        #STUB: this handles the case where playback is paused (DONE)
        elif not playback.get("is_playing"):
            if last != "paused":
                print("Stopped playing.")
                last = "paused"



        #STUB: This handles the case where a new track starts playing (DONE)
        elif (track_id := playback["item"].get("id")) != last:
            print(line)
            last = track_id
            
                

        time.sleep(5)


    