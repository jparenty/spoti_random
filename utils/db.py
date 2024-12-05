import json
import os
import click

from utils.spotify import SpotifyApi
from utils.user import User
from utils.definitions import CACHE_PATH
# DB is local json files

from utils.db_utils.track import Track
import utils.db_utils.playlists as playlist

class DbUtil(SpotifyApi):

    def __init__(self, user_name) -> None:
        #@click.command()
        def _get_user(user_name):
            user = User.get_user(user_name)

            if user == None:
                new_user = click.prompt(click.style("Unknown user, create user? (True/False)", fg='yellow'), type=bool)
                if new_user:
                    spotify_id = click.prompt(click.style("Enter spotify ID", fg='yellow'), type=str)
                    user = User(user_name=user_name, spotify_id=spotify_id)
                    self._cache_data(f"{user_name}/user.json", user.to_json())
                else:
                    return Exception("Unknown user, exiting...")

            return user       

        self.user = _get_user(user_name)
        
    def _check_cache_exists(self, path):
        if os.path.exists(f"{CACHE_PATH}/{path}"):
            return True
        else:
            return False
        
    def _cache_data(self, path, data):
        path = f"{CACHE_PATH}/{path}"
        extension = path.split(".")[-1]
        if extension == "json":
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            if isinstance(data, list):
                data = [obj.to_dict() for obj in data]
            else:
                if not isinstance(data, dict):
                    data = data.to_dict()
    
            file = open(path, "w")

            file.write(json.dumps(data, indent=4))
            file.close
            return
        elif extension == "csv":
            data.to_csv(f"{CACHE_PATH}/{path}")
            return
        else:
            return TypeError("Data type not supported by cache_data method")
    
    @staticmethod
    def _read_cache_playlists(path):
        raise NotImplementedError
    
    @staticmethod
    def _read_cache_tracks(path : str):
        with open(f"{CACHE_PATH}/{path}") as f:
            data = json.load(f)
        
        data = [Track(**d) for d in data]
        return data

    @staticmethod
    def _cache_artists(oath):
        raise NotImplemented
        # path = f"{CACHE_PATH}/{path}"
        # directory = os.path.dirname(path)
        
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
    
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


    def _read_cache(self, path):
        breakpoint()
        with open(f"{CACHE_PATH}/{path}") as f:
            data = json.load(f)
            return data

    def _add_songs_details(clean_tracks):
        pass

    def _update_user_add_playlists(self, playlists: dict):
        ## flag user playlists that are written on the spotify account

        # read db
        with open("playlists.json") as f_in:
                user_playlists = json.load(f_in)  

        # try to flag the user playlists
        for playlist in list(playlists.keys()):
            try:
                user_playlists[playlist] = playlists[playlist]["spotify_id"]
            except:
                click.secho("ERROR: genre playlist not in user's playlist", fg="red")
        
        # update db
        self._cache_data(f"{self.user.user_name}/playlists.json", playlists)
    
    def _get_tracks_genre_from_artist(self, track):
        if self._check_cache_exists("artists_info.json"):
            artists_cache = self._read_cache("artists_info.json")
        else: 
            artists_cache = {}

        genre_tracks, artist = self.user.connection.get_tracks_genre_from_artist(track, artists_cache)    
        # cache_artist_data
        if artist:
            self._cache_data("/artist_info.json", artist)

        return genre_tracks

    def get_user_tracks(self):
        # check if songs by genre cache exists
        if self._check_cache_exists(f"{self.user.user_name}/genre_clean_songs.json"):
            click.secho("Reading cache genre songs...", fg="green")
            genre_tracks = self._read_cache_tracks(f"{self.user.user_name}/genre_clean_songs.json") 

        else:
            #check if cache liked songs exists
            if self._check_cache_exists(f"{self.user.user_name}/clean_songs.json"):
                click.secho("Reading cache liked songs...", fg="yellow")
                tracks_raw = self._read_cache_tracks(f"{self.user.user_name}/clean_songs.json") 

            else:
                # fetch liked songs from spotify account with api
                click.secho("No cache! Fetching recent liked songs...", fg="red")

                prompt_text = click.style("Enter the number of songs in spotify library (approx. round up)", fg="yellow", bold=True)
                songs_number = click.prompt(prompt_text, type=int) 
                tracks_raw = self.user.connection.fetch_liked_songs(songs_number)
                
                click.secho("Caching data...", fg="green")
                self._cache_data(f"{self.user.user_name}/clean_songs.json", tracks_raw)

            #assign genres to song based on artists genre
            genre_tracks = self._get_tracks_genre_from_artist(tracks_raw)

            # cache songs with genre information
            self._cache_data(f"{self.user.user_name}/genre_clean_songs.json", genre_tracks)


        return genre_tracks

    # not very useful
    def update_user_delete_playlists(self, playlists: dict):
        user_playlists = self._read_cache_playlists(f"{self.user.user_name}/playlists.json")
        playlist.update_user_delete_playlists(user_playlists)

    def generate_playlists(self, tracks):
        playlists = playlist.generate_playlists(self, tracks)
        return playlists

    def get_playlists_stats(self, playlists):
        playlists_stats = playlist.get_playlists_stats(self, playlists)
        return playlists_stats

    def user_write_spotify_playlists(self, playlists):
        self.user.connection.write_spotify_playlist(self.user.spotify_id, playlists)

    def user_delete_all_playlists(self):
        user_playlists = self.user.connection.update_user_delete_all_playlists()
        # update user playlists 
        self._cache_data(f"{self.user.user_name}/playlists.json", user_playlists)

    def _get_last_track(self):
        user_tracks = self._read_cache_tracks(f"{self.user.user_name}/clean_songs.json")
        return user_tracks[0]

    def _user_add_tracks(self, new_tracks):
        user_tracks = self._read_cache_tracks(f"{self.user.user_name}/genre_clean_songs.json")
        user_tracks.extend(new_tracks)
    
        self._cache_data(f"{self.user.user_name}/genre_clean_songs.json", user_tracks)

    def update_liked_songs(self):
        track.update_liked_songs()