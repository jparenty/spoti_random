# db is local json files
import json
import os

from .definitions import CACHE_PATH

# from utils.user import User
# from utils.db_utils.track import Track
# import utils.db_utils.playlists as playlist
# from .user import User

def check_cache_exists(path):
    if os.path.exists(f"{CACHE_PATH}/{path}"):
        return True
    else:
        return False

def cache_data(path, data):
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



# class Database():

#     def __init__(self, user: User) -> None:
#         self.user = user



#     @staticmethod
#     def _read_cache_playlists(path):
#         raise NotImplementedError


#     @staticmethod
#     def _cache_artists(oath):
#         raise NotImplemented
#         # path = f"{CACHE_PATH}/{path}"
#         # directory = os.path.dirname(path)
        
#         # if not os.path.exists(directory):
#         #     os.makedirs(directory)
    
#     def _read_cache(self, path):
#         with open(f"{CACHE_PATH}/{path}") as f:
#             data = json.load(f)
#             return data

#     def _add_songs_details(clean_tracks):
#         pass

#     def _update_user_add_playlists(self, playlists: dict):
#         ## flag user playlists that are written on the spotify account

#         # read db
#         with open("playlists.json") as f_in:
#                 user_playlists = json.load(f_in)  

#         # try to flag the user playlists
#         for playlist in list(playlists.keys()):
#             try:
#                 user_playlists[playlist] = playlists[playlist]["spotify_id"]
#             except:
#                 click.secho("ERROR: genre playlist not in user's playlist", fg="red")
        
#         # update db
#         self._cache_data(f"{self.user.user_name}/playlists.json", playlists)
    

#     def update_trakcs(self):
#         self.user.update_tracks()

#     # not very useful
#     def update_user_delete_playlists(self, playlists: dict):
#         user_playlists = self._read_cache_playlists(f"{self.user.user_name}/playlists.json")
#         user_playlists = playlist.update_user_delete_playlists(user_playlists)
#         self._cache_data(f"{self.user.user_name}/playlists.json", user_playlists)

#     def generate_playlists(self, tracks):
#         playlists = playlist.generate_playlists(self, tracks)
#         return playlists

#     def get_playlists_stats(self, playlists):
#         playlists_stats = playlist.get_playlists_stats(self, playlists)
#         return playlists_stats

#     def user_write_spotify_playlists(self, playlists):
#         self.user.connection.write_spotify_playlist(self.user.spotify_id, playlists)

#     def user_delete_all_playlists(self):
#         user_playlists = self.user.connection.update_user_delete_all_playlists()
#         # update user playlists 
#         self._cache_data(f"{self.user.user_name}/playlists.json", user_playlists)

#     def _get_last_track(self):
#         user_tracks = self._read_cache_tracks(f"{self.user.user_name}/clean_songs.json")
#         return user_tracks[0]

#     def _user_add_tracks(self, new_tracks):
#         user_tracks = self._read_cache_tracks(f"{self.user.user_name}/genre_clean_songs.json")
#         user_tracks.extend(new_tracks)
    
#         self._cache_data(f"{self.user.user_name}/genre_clean_songs.json", user_tracks)

#     def generate_random_track():
#         raise NotImplementedError
        

#     def update_liked_songs(self):
#         track.update_liked_songs()