from ytmusicapi.continuations import get_continuations
from ytmusicapi.parsers.uploads import parse_uploaded_items

def if_continuation(self, endpoint, body, limit, items, results):
    if 'continuations' in results:
        request_func = lambda additionalParams: self._send_request(
            endpoint, body, additionalParams)
        parse_func = lambda contents: parse_uploaded_items(contents)
        remaining_limit = None if limit is None else (limit - len(items))
        items.extend(
            get_continuations(results, 'musicShelfContinuation', remaining_limit, request_func,
                                parse_func))    