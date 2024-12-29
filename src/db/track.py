class Track:
    def __init__(self, name, id, url, album, artists, genre, uri : str = None):
        self.name = name
        self.id = id
        self.url = url
        self.album = album
        self.artists = artists
        self.genre = genre
        self.uri = uri

    def to_dict(self):
        d = {
            "name" : self.name,
            "id" : self.id,
            "url" : self.url,
            "album" : self.album,
            "artists" : self.artists,
            "genre": self.genre,
            "uri" : self.uri,
        }
        return d
