import spotipy
from spotipy.oauth2 import SpotifyOAuth

import time
import json
import click

from .definitions import CACHE_PATH
from .db.track import Track
from db_utils import cache_data

class SpotifyApi():
    
    def __init__(self, user_name, spotify_id) -> None:
        def _auth_02(user_name):
            scope = 'user-library-read playlist-modify-private playlist-read-private playlist-modify-public'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, show_dialog = True, username=user_name))
            return sp
        

        self.request_count = 0
        self.last_request = time.time()
        self.user_name = user_name
        self.spotify_id = spotify_id
        self.sp = _auth_02(self.user_name)
        print(self.sp.current_user())
        click.secho("Authentification successfull", fg="green")

    def __check_count(self):
        current_request = time.time()
        # if it's been more than 30s since last request
        print(f"API call count: {self.request_count}")
        if current_request - self.last_request > 30:
            # reset counter to 0
            self.request_count = 0
            return
        else:
            self.last_request = time.time()
            self.request_count = self.request_count + 1
            if self.request_count % 75 == 0:
                click.secho("Slow down... API needs to chill", fg="yellow")
                for i in range(15, 0, -1):
                    print(f"sleeping {i}")
                    time.sleep(1)

    
    def fetch_liked_songs(self, songs_number: int) -> list[Track]:
        #! a revoir -> cette methode devrait seulement gerer l appel à l api
        tracks = []
        offset = 0
        for i in range(50, songs_number+50, 50):
            print(f"fetching songs... count: {i}...")
            self.__check_count()
            sample_saved_tracks = self.sp.current_user_saved_tracks(limit = 50, offset=offset)["items"]
            clean_sample = [{k: v for k, v in d.items() if k != 'added_at'} for d in sample_saved_tracks]
            tracks_sample = [Track(
                    name = data["track"]["name"],
                    id = data["track"]["id"],
                    uri = data["track"]["uri"],
                    album = data["track"]["album"]["name"],
                    artists = data["track"]["artists"],
                    genre = []
                ) for data in clean_sample]

            offset = i
            tracks.extend(tracks_sample)
            print(len(tracks))

        return tracks

    def get_new_tracks(self, last_track):
        new_tracks = []
        offset = 0

        click.secho("Fetching new tracks", fg="green")
        while True:
            click.secho(f"fetching sample {offset+50}...")

            self.__check_count()
            
            sample = self.sp.current_user_saved_tracks(limit = 50, offset=offset)["items"]

            # check if sample contains last tracks -> add sample until last track and break
            sample_ids = [track["track"]["id"] for track in sample]
            if last_track["track_id"] in sample_ids:
                last_track_i = sample_ids.index(last_track["track_id"])
                sample = sample[0:last_track_i]
                
                new_tracks.extend(sample)
                break

            new_tracks.extend(sample)
            print(len(new_tracks))
            offset += 50

        return new_tracks

    def get_tracks_genre_from_artist(self, tracks: list[Track], artist_cache: dict):
        ##!! cette methode ne doit pas gérer les appeles à la db local
        # cette methode devrait juste gérer l appel pour choper genre artiste et c est tout
        # deplacer le reste de la logique dans db/artists.py
        update_cache = False

        for index, track in enumerate(tracks):
            genres = set()
            for artist in track.artists:
                # check if artist exists in cache
                if artist["id"] not in list(artist_cache.keys()):
                    print(f"Fetch artist info '{artist['name']}' info for '{track.name}'")
                    self.__check_count()
                    # fetch artist data
                    artist_info = self.sp.artist(artist["id"])

                    artist_cache[artist["id"]] = artist_info
                    update_cache = True

                else:
                    # read artist info from cache
                    click.secho(f"Read artist info '{artist['name']}' info for '{track.name}'", fg="green")
                    artist_info = artist_cache[artist["id"]]
                
                genres = genres.union(set(artist_info["genres"]))
        
            track.genre = list(genres)
            
            # cache_artist_data
            if index % 50 == 0 and update_cache == True:
                cache_data("/artist_info.json", artist_cache)
                update_cache = False
        
        return tracks

    def write_spotify_playlist(self, spotfy_id, playlists: dict):
        #! a revoir, devrait seulment gerer l appel à l api
        
        sorted_playlists = dict(sorted(playlists.items(), reverse=True))

        for playlist in sorted_playlists:
            # create genre
            print("creating new playlist: " + str(playlist) + " ...")
            #self.__check_count()
            new_playlist = self.sp.user_playlist_create(spotfy_id, str(playlist), public=False, description = playlists[playlist]["description"])
            request_count =+ 1

            # save spotify playlist_id and update later user's playlists
            playlists[playlist]["spotify_id"] = new_playlist["id"]

            # add songs' playlist to spotify playlist - add songs 100 by 100
            for i in range(0,len(playlists[playlist]["tracks"]),100):
                sub = playlists[playlist]["tracks"][i:i+100]
                songs_uri = []
                for track in sub:
                    songs_uri.append(track["track_uri"])

                #self.__check_count()
                self.sp.user_playlist_add_tracks(self.user_name, new_playlist["id"], songs_uri)
                request_count =+ 1
        
        return playlists
    
    def update_user_delete_all_playlists(self):
    
        # read cache playlists
        with open("playlists.json") as f_in:
                user_playlists = json.load(f_in)  
        
        for playlist in user_playlists:
            if "spotify_id" in list(user_playlists[playlist].keys()):
                print(f"Generated playlist {playlist} removed from account!")
                self.__check_count()
                self.sp.current_user_unfollow_playlist(user_playlists[playlist]["spotify_id"])
                request_count =+ 1
                # remove spotify id from the playlist dict
                user_playlists[playlist].pop("spotify_id")
            else:
                continue
        
        return

    def fetch_playlist(self, playlist_id):
        
        playlist = self.sp.playlist(playlist_id)

        return playlist
            
    # OLD
    def delete_generated_playlist(self):

        # get user's playlists
        user_playlists = self.sp.user_playlists(self.spotify_id)["items"]
        generated_playlists = []
    
        for playlist in user_playlists:
            # spot generated playlist and get its id
            playlist_description = playlist["description"]
            if ":magic_jean:" in playlist_description:
                print("Generated playlist spoted!")
                generated_playlists.append(playlist["id"])
        
        # delete generated playlist from user's account
        for delete_playlist in generated_playlists:
            self.sp.current_user_unfollow_playlist(delete_playlist)
            print("Generated playlist deleted!")

        return



