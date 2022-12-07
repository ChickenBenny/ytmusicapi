from mixins._utils import validate_order_parameter, prepare_order_params
from typing import List, Dict

body_changer = {
    "upload_songs": "FEmusic_library_privately_owned_tracks",
    "upload_albums": "FEmusic_library_privately_owned_releases",
    "upload_artists": "FEmusic_library_privately_owned_artists"
}

def get_mult_library(self, type, limit: int = 25, order: str = None) -> List[Dict]:
    self._check_auth()
    endpoint = 'browse'
    body = {"browseId": body_changer['type']}
    validate_order_parameter(order)
    if order is not None:
        body["params"] = prepare_order_params(order)
    response = self._send_request(endpoint, body)
    return endpoint, body, response