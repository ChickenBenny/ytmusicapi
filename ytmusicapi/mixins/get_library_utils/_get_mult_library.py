from mixins._utils import validate_order_parameter, prepare_order_params
from typing import List, Dict

def get_mult_library(self, browseId: str, limit = None) -> Dict:
    self._check_auth()
    endpoint = 'browse'
    body = {"browseId": browseId}
    response = self._send_request(endpoint, body)
    return endpoint, body, response