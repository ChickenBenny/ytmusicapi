from typing import List, Dict, Union
from ._utils import validate_order_parameter, prepare_order_params
from ytmusicapi.parsers.library import parse_library_albums, parse_library_artists, get_library_contents
from ytmusicapi.continuations import get_continuations
from ytmusicapi.parsers.uploads import parse_uploaded_items
from ytmusicapi.navigation import *
from ytmusicapi.helpers import *
from ytmusicapi.parsers.albums import parse_album_header


class UploadsMixinGetLibrary:
    def get_library_upload_songs(self, limit: int = 25, order: str = None) -> List[Dict]:
        """
        Returns a list of uploaded songs

        :param limit: How many songs to return. `None` retrieves them all. Default: 25
        :param order: Order of songs to return. Allowed values: 'a_to_z', 'z_to_a', 'recently_added'. Default: Default order.
        :return: List of uploaded songs.

        Each item is in the following format::

            {
              "entityId": "t_po_CICr2crg7OWpchDpjPjrBA",
              "videoId": "Uise6RPKoek",
              "artists": [{
                'name': 'Coldplay',
                'id': 'FEmusic_library_privately_owned_artist_detaila_po_CICr2crg7OWpchIIY29sZHBsYXk',
              }],
              "title": "A Sky Full Of Stars",
              "album": "Ghost Stories",
              "likeStatus": "LIKE",
              "thumbnails": [...]
            }
        """
        self._check_auth()
        endpoint = 'browse'
        body = {"browseId": "FEmusic_library_privately_owned_tracks"}
        validate_order_parameter(order)
        if order is not None:
            body["params"] = prepare_order_params(order)
        response = self._send_request(endpoint, body)
        results = get_library_contents(response, MUSIC_SHELF)
        if results is None:
            return []
        songs = parse_uploaded_items(results['contents'][1:])

        if 'continuations' in results:
            request_func = lambda additionalParams: self._send_request(
                endpoint, body, additionalParams)
            remaining_limit = None if limit is None else (limit - len(songs))
            songs.extend(
                get_continuations(results, 'musicShelfContinuation', remaining_limit, request_func,
                                  parse_uploaded_items))

        return songs    

    def get_library_upload_albums(self, limit: int = 25, order: str = None) -> List[Dict]:
        """
        Gets the albums of uploaded songs in the user's library.

        :param limit: Number of albums to return. `None` retrives them all. Default: 25
        :param order: Order of albums to return. Allowed values: 'a_to_z', 'z_to_a', 'recently_added'. Default: Default order.
        :return: List of albums as returned by :py:func:`get_library_albums`
        """
        self._check_auth()
        body = {'browseId': 'FEmusic_library_privately_owned_releases'}
        validate_order_parameter(order)
        if order is not None:
            body["params"] = prepare_order_params(order)
        endpoint = 'browse'
        response = self._send_request(endpoint, body)
        return parse_library_albums(
            response,
            lambda additionalParams: self._send_request(endpoint, body, additionalParams), limit)

    def get_library_upload_artists(self, limit: int = 25, order: str = None) -> List[Dict]:
        """
        Gets the artists of uploaded songs in the user's library.

        :param limit: Number of artists to return. `None` retrieves them all. Default: 25
        :param order: Order of artists to return. Allowed values: 'a_to_z', 'z_to_a', 'recently_added'. Default: Default order.
        :return: List of artists as returned by :py:func:`get_library_artists`
        """
        self._check_auth()
        body = {'browseId': 'FEmusic_library_privately_owned_artists'}
        validate_order_parameter(order)
        if order is not None:
            body["params"] = prepare_order_params(order)
        endpoint = 'browse'
        response = self._send_request(endpoint, body)
        return parse_library_artists(
            response,
            lambda additionalParams: self._send_request(endpoint, body, additionalParams), limit)

    def get_library_upload_artist(self, browseId: str, limit: int = 25) -> List[Dict]:
        """
        Returns a list of uploaded tracks for the artist.

        :param browseId: Browse id of the upload artist, i.e. from :py:func:`get_library_upload_songs`
        :param limit: Number of songs to return (increments of 25).
        :return: List of uploaded songs.

        Example List::

            [
              {
                "entityId": "t_po_CICr2crg7OWpchDKwoakAQ",
                "videoId": "Dtffhy8WJgw",
                "title": "Hold Me (Original Mix)",
                "artists": [
                  {
                    "name": "Jakko",
                    "id": "FEmusic_library_privately_owned_artist_detaila_po_CICr2crg7OWpchIFamFra28"
                  }
                ],
                "album": null,
                "likeStatus": "LIKE",
                "thumbnails": [...]
              }
            ]
        """
        self._check_auth()
        body = {'browseId': browseId}
        endpoint = 'browse'
        response = self._send_request(endpoint, body)
        results = nav(response, SINGLE_COLUMN_TAB + SECTION_LIST_ITEM + MUSIC_SHELF)
        if len(results['contents']) > 1:
            results['contents'].pop(0)

        items = parse_uploaded_items(results['contents'])

        if 'continuations' in results:
            request_func = lambda additionalParams: self._send_request(
                endpoint, body, additionalParams)
            parse_func = lambda contents: parse_uploaded_items(contents)
            remaining_limit = None if limit is None else (limit - len(items))
            items.extend(
                get_continuations(results, 'musicShelfContinuation', remaining_limit, request_func,
                                  parse_func))

        return items

    def get_library_upload_album(self, browseId: str) -> Dict:
        """
        Get information and tracks of an album associated with uploaded tracks

        :param browseId: Browse id of the upload album, i.e. from i.e. from :py:func:`get_library_upload_songs`
        :return: Dictionary with title, description, artist and tracks.

        Example album::

            {
              "title": "18 Months",
              "type": "Album",
              "thumbnails": [...],
              "trackCount": 7,
              "duration": "24 minutes",
              "audioPlaylistId": "MLPRb_po_55chars",
              "tracks": [
                {
                  "entityId": "t_po_22chars",
                  "videoId": "FVo-UZoPygI",
                  "title": "Feel So Close",
                  "duration": "4:15",
                  "duration_seconds": 255,
                  "artists": None,
                  "album": {
                    "name": "18 Months",
                    "id": "FEmusic_library_privately_owned_release_detailb_po_55chars"
                  },
                  "likeStatus": "INDIFFERENT",
                  "thumbnails": None
                },
        """
        self._check_auth()
        body = {'browseId': browseId}
        endpoint = 'browse'
        response = self._send_request(endpoint, body)
        album = parse_album_header(response)
        results = nav(response, SINGLE_COLUMN_TAB + SECTION_LIST_ITEM + MUSIC_SHELF)
        album['tracks'] = parse_uploaded_items(results['contents'])
        album['duration_seconds'] = sum_total_duration(album)
        return album