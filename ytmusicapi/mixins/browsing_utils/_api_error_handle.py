from ytmusicapi.parsers.playlists import parse_playlist_items
from ytmusicapi.parsers.browsing import *

def api_return_none(artist, results):
    if 'musicShelfRenderer' in results[0]:  # API sometimes does not return songs
        musicShelf = nav(results[0], MUSIC_SHELF)
        if 'navigationEndpoint' in nav(musicShelf, TITLE):
            artist['songs']['browseId'] = nav(musicShelf, TITLE + NAVIGATION_BROWSE_ID)
        artist['songs']['results'] = parse_playlist_items(musicShelf['contents'])    