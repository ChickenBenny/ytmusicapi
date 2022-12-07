import requests
import ntpath
import os
from typing import List, Dict, Union
from raise_utils import check_path, support_exception
from ytmusicapi.helpers import *
from ytmusicapi.navigation import *


class UploadsMixin:

    def upload_song(self, filepath: str) -> Union[str, requests.Response]:
        """
        Uploads a song to YouTube Music

        :param filepath: Path to the music file (mp3, m4a, wma, flac or ogg)
        :return: Status String or full response
        """
        self._check_auth()
        check_path(filepath)
        support_exception(filepath)

        headers = self.headers.copy()
        upload_url = "https://upload.youtube.com/upload/usermusic/http?authuser=%s" % headers[
            'x-goog-authuser']
        filesize = os.path.getsize(filepath)
        body = ("filename=" + ntpath.basename(filepath)).encode('utf-8')
        headers.pop('content-encoding', None)
        headers['content-type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        headers['X-Goog-Upload-Command'] = 'start'
        headers['X-Goog-Upload-Header-Content-Length'] = str(filesize)
        headers['X-Goog-Upload-Protocol'] = 'resumable'
        response = requests.post(upload_url, data=body, headers=headers, proxies=self.proxies)
        headers['X-Goog-Upload-Command'] = 'upload, finalize'
        headers['X-Goog-Upload-Offset'] = '0'
        upload_url = response.headers['X-Goog-Upload-URL']
        with open(filepath, 'rb') as file:
            response = requests.post(upload_url, data=file, headers=headers, proxies=self.proxies)

        if response.status_code == 200:
            return 'STATUS_SUCCEEDED'
        else:
            return response

    def delete_upload_entity(self, entityId: str) -> Union[str, Dict]:  # pragma: no cover
        """
        Deletes a previously uploaded song or album

        :param entityId: The entity id of the uploaded song or album,
            e.g. retrieved from :py:func:`get_library_upload_songs`
        :return: Status String or error
        """
        self._check_auth()
        endpoint = 'music/delete_privately_owned_entity'
        if 'FEmusic_library_privately_owned_release_detail' in entityId:
            entityId = entityId.replace('FEmusic_library_privately_owned_release_detail', '')

        body = {"entityId": entityId}
        response = self._send_request(endpoint, body)

        if 'error' not in response:
            return 'STATUS_SUCCEEDED'
        else:
            return response['error']
