from spotify import spotify_logic  # Import the get_client and describe functions from spotify.py




if __name__ == "__main__":
    try:
        spotify_logic()  # Call the spotify_logic function to start the program
    except KeyboardInterrupt:
        print("\nStopped.")
