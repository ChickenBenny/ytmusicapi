from ytmusicapi.parsers.browsing import *
from ytmusicapi.helpers import YTM_DOMAIN, sum_total_duration
from browsing_utils import _browsing_results, api_return_none
from ytmusicapi.parsers.albums import parse_album_header
from ytmusicapi.parsers.playlists import parse_playlist_items

class BrowsingSong:
    def get_album_browse_id(self, audioPlaylistId: str):
        """
        Get an album's browseId based on its audioPlaylistId

        :param audioPlaylistId: id of the audio playlist  (starting with `OLAK5uy_`)
        :return: browseId (starting with `MPREb_`)
        """
        params = {"list": audioPlaylistId}
        response = self._send_get_request(YTM_DOMAIN + "/playlist", params)
        matches = re.findall(r"\"MPRE.+?\"", response)
        browse_id = None
        if len(matches) > 0:
            browse_id = matches[0].encode('utf8').decode('unicode-escape').strip('"')
        return browse_id

    def get_album(self, browseId: str) -> Dict:
        """
        Get information and tracks of an album

        :param browseId: browseId of the album, for example
            returned by :py:func:`search`
        :return: Dictionary with album and track metadata.

        Each track is in the following format::

            {
              "title": "Revival",
              "type": "Album",
              "thumbnails": [],
              "description": "Revival is the...",
              "artists": [
                {
                  "name": "Eminem",
                  "id": "UCedvOgsKFzcK3hA5taf3KoQ"
                }
              ],
              "year": "2017",
              "trackCount": 19,
              "duration": "1 hour, 17 minutes",
              "audioPlaylistId": "OLAK5uy_nMr9h2VlS-2PULNz3M3XVXQj_P3C2bqaY",
              "tracks": [
                {
                  "videoId": "iKLU7z_xdYQ",
                  "title": "Walk On Water (feat. Beyoncé)",
                  "artists": [
                    {
                      "name": "Eminem",
                      "id": "UCedvOgsKFzcK3hA5taf3KoQ"
                    }
                  ],
                  "album": "Revival",
                  "likeStatus": "INDIFFERENT",
                  "thumbnails": null,
                  "isAvailable": true,
                  "isExplicit": true,
                  "duration": "5:03",
                  "duration_seconds": 303,
                  "feedbackTokens": {
                    "add": "AB9zfpK...",
                    "remove": "AB9zfpK..."
                  }
                }
              ],
              "other_versions": [
                {
                  "title": "Revival",
                  "year": "Eminem",
                  "browseId": "MPREb_fefKFOTEZSp",
                  "thumbnails": [...],
                  "isExplicit": false
                },
              ],
              "duration_seconds": 4657
            }
        """
        response, results = _browsing_results(self, 'browse', {"browseId": browseId}, SINGLE_COLUMN_TAB + SECTION_LIST_ITEM + MUSIC_SHELF)
        album = parse_album_header(response)
        album['tracks'] = parse_playlist_items(results['contents'])
        results = nav(response, SINGLE_COLUMN_TAB + SECTION_LIST + [1] + CAROUSEL, True)
        if results is not None:
            album['other_versions'] = parse_content_list(results['contents'], parse_album)
        album['duration_seconds'] = sum_total_duration(album)
        for i, _ in enumerate(album['tracks']):
            album['tracks'][i]['album'] = album['title']
            album['tracks'][i]['artists'] = album['artists']

        return album