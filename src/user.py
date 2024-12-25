import json
import click
import os
import random

from .spotify import SpotifyApi
from .definitions import CACHE_PATH

from .db.track import Track 
from .db_utils import check_cache_exists, cache_data

class User():

    def __init__(self, user_name: str):
        def _get_user(user_name):
            try:
                with open(f"{CACHE_PATH}/{user_name}/user.json") as f:
                    user = json.load(f)
                    user = User(
                        user_name = user["user_name"],
                        spotify_id = user["spotify_id"]
                    )
                    user.spotify_id = user.spotify_id

            except FileNotFoundError:
                user = None
            except Exception as e:
                return e
            
            if user == None:
                new_user = click.prompt(click.style("Unknown user, create user? (True/False)", fg='yellow'), type=bool)
                if new_user:
                    spotify_id = click.prompt(click.style("Enter spotify ID", fg='yellow'), type=str)
                    user = User(user_name=user_name, spotify_id=spotify_id)
                    cache_data(f"{user_name}/user.json", user.to_json())
                else:
                    return Exception("Unknown user, exiting...")

            return spotify_id

        spotify_id = _get_user(user_name)
        self.user_name = user_name
        self.spotify_id = spotify_id
        self.connection = SpotifyApi(user_name=user_name, spotify_id=spotify_id)
        self.tracks: list[Track] = self._get_tracks()
        self.playlits = None


    
    @staticmethod
    def _read_cache_tracks(path : str):
        with open(f"{CACHE_PATH}/{path}") as f:
            data = json.load(f)
        
        data = [Track(**d) for d in data]
        return data

    @staticmethod
    def _cache_tracks(path: str, tracks : list[Track]):
        path = f"{CACHE_PATH}/{path}"
        directory = os.path.dirname(path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)    

        d_tracks = [track.to_dict() for track in tracks]

        file = open(path, "w")
        file.write(json.dumps(d_tracks, indent=4))
        file.close


    def to_json(self):
        user = {
            "user_name" : self.user_name,
            "spotify_id" : self.spotify_id
        }
        return user

    def _get_tracks_genre_from_artist(self, track):
        if check_cache_exists("artists_info.json"):
            artists_cache = self._read_cache_tracks("artists_info.json")
        else: 
            artists_cache = {}

        genre_tracks = self.connection.get_tracks_genre_from_artist(track, artists_cache)    


        return genre_tracks


    def _get_tracks(self):
        # check if songs by genre cache exists
        if check_cache_exists(f"{self.user_name}/tracks_genre.json"):
            click.secho("Tracks already fetched...", fg="green")
            tracks_genre = self._read_cache_tracks(f"{self.user_name}/tracks_genre.json") 

        else:
            #check if cache liked songs exists
            if check_cache_exists(f"{self.user_name}/clean_songs.json"):
                click.secho("Reading cache liked songs...", fg="yellow")
                tracks_no_genre = self._read_cache_tracks(f"{self.user_name}/clean_songs.json") 

            else:
                # fetch liked songs from spotify account with api
                click.secho("No cache! Fetching recent liked songs...", fg="red")

                prompt_text = click.style("Enter the number of songs in spotify library (approx. round up)", fg="yellow", bold=True)
                songs_number = click.prompt(prompt_text, type=int) 
                tracks_genre = self._fetch_liked_songs(songs_number)
                
                click.secho("Caching data...", fg="green")
                self._cache_tracks(f"{self.user_name}/tracks_genre.json", tracks_genre)
                #self._cache_tracks(f"{self.user_name}/clean_songs.json", tracks_raw)

            # #assign genres to song based on artists genre
            # tracks_genre = self._get_tracks_genre_from_artist(tracks_raw)

            # cache songs with genre information

        return tracks_genre
    
    def _fetch_liked_songs(self, songs_number: int) -> list[Track]:
        #! a revoir -> cette methode devrait seulement gerer l appel à l api
        tracks_genre = []
        offset = 0
        for i in range(50, songs_number+50, 50):
            # get liked tracks from spotify
            tracks_sample = self.connection.fetch_liked_tracks(offset)    
            # assign genre on liked tracks sample
            tracks_genre_sample = self._get_tracks_genre_from_artist(tracks_sample)
            tracks_genre.extend(tracks_genre_sample)
            print(len(tracks_genre))
            
            offset = i

        return tracks_genre
    
    def _get_last_track(self):
        user_tracks = self._read_cache_tracks(f"{self.user_name}/clean_songs.json")
        return user_tracks[0]

    def _user_add_tracks(self, new_tracks):
        user_tracks = self._read_cache_tracks(f"{self.user_name}/genre_clean_songs.json")
        user_tracks.extend(new_tracks)
        self._cache_tracks(f"{self.user_name}/genre_clean_songs.json", user_tracks)

    def update_tracks(self):
        
        if check_cache_exists(f"{self.user_name}/genre_clean_songs.json"):
            last_track = self._get_last_track()
            new_tracks_raw = self.connection.get_new_tracks(last_track)

            new_tracks = self._get_tracks_genre_from_artist(new_tracks_raw)
            self._user_add_tracks(new_tracks)

            click.secho(f"Liked tracks successfully updated for {self.user_name}", fg="green")
        
        else:
            click.secho(f"No saved songs to update for {self.user_name}", fg="red")
            
    def generate_random_track(self):
        random_track_index = random.randint(0, len(self.tracks))
        track_url = self.tracks[random_track_index].url
        return print(track_url)