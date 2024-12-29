import json
import click
import os
import random

from .spotify import SpotifyApi
from .definitions import CACHE_PATH

from .db.track import Track 
from .db.device import Device 
from .db_utils import check_cache_exists, cache_data, read_cache

class User():

    def __init__(self, user_name: str):
        def _get_spotify_id(user_name):
            try:
                with open(f"{CACHE_PATH}/{user_name}/user.json") as f:
                    user = json.load(f)
                    spotify_id = user["spotify_id"]

            except FileNotFoundError:
                new_user = click.prompt(click.style("Unknown user, create user? (True/False)", fg='yellow'), type=bool)
                if new_user:
                    spotify_id = click.prompt(click.style("Enter spotify ID", fg='yellow'), type=str)
                else:
                    return Exception("Unknown user, exiting...")
            
            except Exception as e:
                raise e
            

            return spotify_id

        self.user_name = user_name
        self.spotify_id = _get_spotify_id(user_name)
        # spotify auth
        self.connection = SpotifyApi(user_name=user_name, spotify_id=self.spotify_id)

        cache_data(f"{self.user_name}/user.json", self.to_json())
        
        self.device : Device = None
        self.playlists = None
        self.tracks : list[Track] = self._get_tracks()

    
    def _read_cache_tracks(self):
        tracks_data = read_cache(f"{self.user_name}/tracks.json")
        
        data = [Track(**d) for d in tracks_data]
        return data

    def _cache_tracks(self, tracks : list[Track]):
        path = f"{self.user_name}/tracks.json"    
        d_tracks = [track.to_dict() for track in tracks]
        cache_data(path, d_tracks)


    def to_json(self):
        user = {
            "user_name" : self.user_name,
            "spotify_id" : self.spotify_id
        }
        return user

    def _get_tracks_genre_from_artist(self, tracks : list[Track]):
        if check_cache_exists("artists.json"):
            artist_cache = read_cache("artists.json")
        else: 
            artist_cache = {}

        update_cache = False

        for index, track in enumerate(tracks):
            genres = set()
            for artist in track.artists:
                # check if artist not in cache
                if artist["id"] not in list(artist_cache.keys()):
                    print(f"Fetch artist '{artist['name']}' for track '{track.name}'")
                    # fetch artist data
                    artist_info = self.connection.get_artist(artist["id"])

                    artist_cache[artist["id"]] = artist_info
                    update_cache = True

                # read artist info from cache
                else:
                    click.secho(f"Read artist '{artist['name']}' for track '{track.name}'", fg="green")
                    artist_info = artist_cache[artist["id"]]
                
                genres = genres.union(set(artist_info["genres"]))
        
            track.genre = list(genres)
            
            # cache_artist_data
            if index % 50 == 0 and update_cache == True:
                cache_data("artists.json", artist_cache)
                update_cache = False
        
        if update_cache == True:
            cache_data("artists.json", artist_cache)
            update_cache = False
        
        return tracks


    def _get_tracks(self):
        # check if songs by genre cache exists
        if check_cache_exists(f"{self.user_name}/tracks.json"):
            click.secho("Tracks already fetched...", fg="green")
            tracks = self._read_cache_tracks() 

        else:
            # fetch liked songs from spotify account with api
            click.secho("No cache! Fetching recent liked songs...", fg="red")

            prompt_text = click.style("Enter the number of songs in spotify library (approx. round up)", fg="yellow", bold=True)
            songs_number = click.prompt(prompt_text, type=int) 
            tracks = self._fetch_liked_songs(songs_number)
            
            click.secho("Caching data...", fg="green")
            self._cache_tracks(tracks)
        return tracks
    
    def _fetch_liked_songs(self, songs_number: int) -> list[Track]:
        tracks = []
        offset = 0

        for i in range(50, songs_number+50, 50):
            # get liked tracks from spotify
            tracks_sample = self.connection.fetch_liked_tracks(offset)    
            # assign genre on liked tracks sample
            tracks_genre_sample = self._get_tracks_genre_from_artist(tracks_sample)
            tracks.extend(tracks_genre_sample)
            print(len(tracks))
            
            offset = i

        return tracks
    
    def _user_add_tracks(self, new_tracks):
        user_tracks = self._read_cache_tracks(f"{self.user_name}/genre_clean_songs.json")
        user_tracks.extend(new_tracks)
        self._cache_tracks(user_tracks)

    def update_tracks(self):
        last_track = self.tracks[0]

        new_tracks_raw = self.connection.get_new_tracks(last_track)
        new_tracks = self._get_tracks_genre_from_artist(new_tracks_raw)

        self._user_add_tracks(new_tracks)
    
    def play_random_track(self):
        # get random liked track
        random_track_index = random.randint(0, len(self.tracks))

        # play random track
        self.connection.play_song(self.device, self.tracks[random_track_index])
