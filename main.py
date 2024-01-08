import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up the authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="-",
                                               client_secret="-",
                                               redirect_uri="http://localhost:2000",
                                               scope="user-top-read playlist-modify-public playlist-modify-private"))

# Fetch top tracks
def get_time_range():
    print("Select the time range:")
    print("1. Short Term (last 4 weeks)")
    print("2. Medium Term (last 6 months)")
    print("3. Long Term (several years)")
    choice = input("Choose 1, 2, or 3: ")
    if choice == "1":
        return 'short_term'
    elif choice == "2":
        return 'medium_term'
    elif choice == "3":
        return 'long_term'
    else:
        print("Invalid choice. Defaulting to short term.")
        return 'short_term'
    
def get_top_tracks(sp, time_range):
    top_tracks = sp.current_user_top_tracks(limit=50, time_range=time_range)
    for index, track in enumerate(top_tracks['items'], start=1):
        print(f"{index}. {track['name']} - {track['artists'][0]['name']}")
    return [track['id'] for track in top_tracks['items']]  # Returns track IDs if needed




def get_top_artists(sp, time_range):
    top_artists = sp.current_user_top_artists(time_range=time_range)

    # Check if any top artists are returned
    if not top_artists['items']:
        print("No top artists found.")
        return

    # Print the list of top artists
    time_range_string = {"short_term": "Past 4 Weeks", "medium_term": "Past 6 Months", "long_term": "Several Years"}
    print(f"Your Top Artists ({time_range_string[time_range]}):")
    for index, artist in enumerate(top_artists['items'], start=1):
        print(f"{index}. {artist['name']}")

def create_playlist(sp, name, public=True, collaborative=False, description=''):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, name, public, collaborative, description)
    return playlist['id']

def add_tracks_to_playlist(sp, playlist_id, track_ids):
    sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlist_id, tracks=track_ids)


def interface(sp):
    time_range = get_time_range()
    options = {
        "1": lambda: get_top_tracks(sp, time_range),
        "2": lambda: get_top_artists(sp, time_range),
        "3": lambda: create_playlist_from_top_tracks(sp, time_range)
    }

    choice = input("What would you like to see? (All options are for the selected time range)\n1. Top Tracks\n2. Top Artists\n3. Create Playlist from Top Tracks\n")

    if choice in options:
        options[choice]()
    else:
        print("Invalid choice. Please select a valid option.")

def create_playlist_from_top_tracks(sp, time_range):
    track_ids = get_top_tracks(sp, time_range)
    if track_ids:
        playlist_name = input("Enter a name for your new playlist: ")
        playlist_id = create_playlist(sp, playlist_name)
        add_tracks_to_playlist(sp, playlist_id, track_ids)
        print(f"Playlist '{playlist_name}' created successfully.")
    else:
        print("No tracks available to add to a playlist.")

interface(sp)
