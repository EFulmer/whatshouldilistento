from collections import namedtuple
import json

import requests 


AS_API_ROOT = 'http://ws.audioscrobbler.com/2.0/'
AS_API_KEY  = '8c5b0975a02e30db77066c474a9c0333'

ArtistInfo = namedtuple('ArtistInfo', ['artist', 'album'])


class ArtistNotFoundException(Exception):
    pass


def get_best_album(artist):
    s = requests.Session()
    s.params = { 'api_key' : AS_API_KEY, 
                 'format' : 'json', 
                 'artist' : artist,
                 'method' : 'artist.gettopalbums',
                 'limit'  : '1'
                 }
    r = s.get(AS_API_ROOT)
    j = json.loads(r.text)
    try:
        album = j[u'topalbums'][u'album'][u'name']
        name = j[u'topalbums'][u'album'][u'artist'][u'name']
        return ArtistInfo(name, album)
    except KeyError as e:
        raise ArtistNotFoundException()

