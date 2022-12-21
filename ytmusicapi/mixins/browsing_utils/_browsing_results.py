from ytmusicapi.parsers.browsing import *

def _browsing_result(self, endpoint, body, params):
    response = self._send_request(endpoint, body)
    results = nav(response, params)
    return response, results