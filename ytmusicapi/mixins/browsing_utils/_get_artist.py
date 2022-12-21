from ytmusicapi.parsers.browsing import *

def _get_artist_info(header, params, results):
    artist = {'description': None, 'views': None}
    subscription_button = _get_subscription_button(header)
    _if_description_shelf(artist, results, params)
    artist['name'] = nav(header, params)
    artist['channelId'] = subscription_button['channelId']
    artist['shuffleId'] = nav(header,
                                ['playButton', 'buttonRenderer'] + NAVIGATION_WATCH_PLAYLIST_ID,
                                True)
    artist['radioId'] = nav(header, ['startRadioButton', 'buttonRenderer']
                            + NAVIGATION_WATCH_PLAYLIST_ID, True)
    artist['subscribers'] = nav(subscription_button,
                                ['subscriberCountText', 'runs', 0, 'text'], True)
    artist['subscribed'] = subscription_button['subscribed']
    artist['thumbnails'] = nav(header, THUMBNAILS, True)
    artist['songs'] = {'browseId': None}
    return artist

def _if_description_shelf(artist, results, params):
    descriptionShelf = find_object_by_key(results, params, True)
    if descriptionShelf:
        artist['description'] = nav(descriptionShelf, DESCRIPTION)
        artist['views'] = None if 'subheader' not in descriptionShelf else descriptionShelf[
            'subheader']['runs'][0]['text']

def _get_subscription_button(header):
    return header['subscriptionButton']['subscribeButtonRenderer']