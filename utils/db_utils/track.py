import click

class Track:
    def __init__(self, track: dict):
        if track["artists"] == []:
            artists = []
        else:
            artists = [artist for artist in track["artists"]]

        self.track_name = track["name"]
        self.track_id = track["id"]
        self.track_uri = track["uri"]
        self.track_album = track["album"]["name"]
        self.track_artists = artists

    def to_dict(self):
        return {'key': self.key, 'value': self.value}

def _get_tracks_genre_from_artist(db, track):
    if db._check_cache_exists("artists_info.json"):
        artists_cache = db._read_cache("artists_info.json")
    else: 
        artists_cache = {}

    genre_tracks, artist = db.user.connection.get_tracks_genre_from_artist(track, artists_cache)    
    # cache_artist_data
    if artist:
        db._cache_data("/artist_info.json", artist)

    return genre_tracks

def get_user_tracks(db):
        
    ##!! à revoir
    # check if songs by genre cache exists
    if db._check_cache_exists(f"{db.user.user_name}/genre_clean_songs.json"):
        click.secho("Reading cache genre songs...", fg="green")
        genre_liked_songs = db._read_cache(f"{db.user.user_name}/genre_clean_songs.json") 

    else:
        #check if cache liked songs exists
        if db._check_cache_exists(f"{db.user.user_name}/clean_songs.json"):
            click.secho("Reading cache liked songs...", fg="yellow")
            clean_liked_songs = db._read_cache(f"{db.user.user_name}/clean_songs.json") 

        else:
            # fetch liked songs from spotify account with api
            click.secho("No cache! Fetching recent liked songs...", fg="red")

            prompt_text = click.style("Enter the number of songs in spotify library (approx. round up)", fg="yellow", bold=True)
            songs_number = click.prompt(prompt_text, type=int) 
            tracks = db.user.connection.fetch_liked_songs(songs_number)
            
            click.secho("Caching data...", fg="green")
            db._cache_data(f"{db.user.user_name}/clean_songs.json", tracks)

        #assign genres to song based on artists genre
        genre_liked_songs = _get_tracks_genre_from_artist(db, tracks)

        # cache songs with genre information
        db._cache_data(f"{db.user.user_name}/genre_clean_songs.json", genre_liked_songs)


    return genre_liked_songs

def update_liked_songs(db):
    
    if db._check_cache_exists(f"{db.user.user_name}/genre_clean_songs.json"):
        last_track = db._get_last_track()
        new_tracks_raw = db.user.connection.get_new_tracks(last_track)
        new_tracks_clean = _clean_tracks(new_tracks_raw)
        new_tracks = _get_tracks_genre_from_artist(db, new_tracks_clean)
        db._user_add_tracks(new_tracks)

        click.secho(f"Liked tracks successfully updated for {db.user.user_name}", fg="green")
    
    else:
        click.secho(f"No saved songs to update for {db.user.user_name}", fg="red")
        