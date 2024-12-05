import click

class Track:
    def __init__(self, name, id, uri, album, artists, genre):
        self.name = name
        self.id = id
        self.uri = uri
        self.album = album
        self.artists = artists
        self.genre = genre

    def to_dict(self):
        d = {
            "name" : self.name,
            "id" : self.id,
            "uri" : self.uri,
            "album" : self.album,
            "artists" : self.artists,
            "genre": self.genre
        }
        return d


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
        