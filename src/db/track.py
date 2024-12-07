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
