from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ExternalUrls:
    spotify: str

@dataclass
class Followers:
    href: Optional[str]
    total: int

@dataclass
class Image:
    url: str
    height: int
    width: int

@dataclass
class Artist:
    id: str
    external_urls: ExternalUrls
    followers: Followers
    genres: List[str]
    href: str
    images: List[Image]
    name: str
    popularity: int
    type: str
    uri: str