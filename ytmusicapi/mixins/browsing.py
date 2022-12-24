from ._utils import get_datestamp
from ytmusicapi.parsers.browsing import *
from raise_utils import raise_get_song, raise_get_lyrics, raise_match, raise_match_signature
from get_library_utils import if_continuation
from browsing_utils import _browsing_results, BrowsingArtist, BrowsingUser, BrowsingSong

class BrowsingMixin:
    def __init__(self):
        self.browsing_artist = BrowsingArtist()
        self.browsing_user = BrowsingUser()
        self.browsing_song = BrowsingSong()

    def get_home(self, limit=3) -> List[Dict]:
        """
        Get the home page.
        The home page is structured as titled rows, returning 3 rows of music suggestions at a time.
        Content varies and may contain artist, album, song or playlist suggestions, sometimes mixed within the same row

        :param limit: Number of rows to return
        :return: List of dictionaries keyed with 'title' text and 'contents' list

        Example list::

            [
                {
                    "title": "Your morning music",
                    "contents": [
                        { //album result
                            "title": "Sentiment",
                            "year": "Said The Sky",
                            "browseId": "MPREb_QtqXtd2xZMR",
                            "thumbnails": [...]
                        },
                        { //playlist result
                            "title": "r/EDM top submissions 01/28/2022",
                            "playlistId": "PLz7-xrYmULdSLRZGk-6GKUtaBZcgQNwel",
                            "thumbnails": [...],
                            "description": "redditEDM • 161 songs",
                            "count": "161",
                            "author": [
                                {
                                    "name": "redditEDM",
                                    "id": "UCaTrZ9tPiIGHrkCe5bxOGwA"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Your favorites",
                    "contents": [
                        { //artist result
                            "title": "Chill Satellite",
                            "browseId": "UCrPLFBWdOroD57bkqPbZJog",
                            "subscribers": "374",
                            "thumbnails": [...]
                        }
                        { //album result
                            "title": "Dragon",
                            "year": "Two Steps From Hell",
                            "browseId": "MPREb_M9aDqLRbSeg",
                            "thumbnails": [...]
                        }
                    ]
                },
                {
                    "title": "Quick picks",
                    "contents": [
                        { //song quick pick
                            "title": "Gravity",
                            "videoId": "EludZd6lfts",
                            "artists": [{
                                    "name": "yetep",
                                    "id": "UCSW0r7dClqCoCvQeqXiZBlg"
                                }],
                            "thumbnails": [...],
                            "album": {
                                "name": "Gravity",
                                "id": "MPREb_D6bICFcuuRY"
                            }
                        },
                        { //video quick pick
                            "title": "Gryffin & Illenium (feat. Daya) - Feel Good (L3V3LS Remix)",
                            "videoId": "bR5l0hJDnX8",
                            "artists": [
                                {
                                    "name": "L3V3LS",
                                    "id": "UCCVNihbOdkOWw_-ajIYhAbQ"
                                }
                            ],
                            "thumbnails": [...],
                            "views": "10M"
                        }
                    ]
                }
            ]

        """
        response, results = _browsing_results(self, 'browse', {"browseId": "FEmusic_home"}, SINGLE_COLUMN_TAB + SECTION_LIST, limit)
        home = []
        home.extend(self.parser.parse_mixed_content(results))
        if_continuation('browse', {"browseId": "FEmusic_home"}, limit, home, results)
        return home

    def get_song(self, videoId: str, signatureTimestamp: int = None) -> Dict:
        """
        Returns metadata and streaming information about a song or video.

        :param videoId: Video id
        :param signatureTimestamp: Provide the current YouTube signatureTimestamp.
            If not provided a default value will be used, which might result in invalid streaming URLs
        :return: Dictionary with song metadata.

        Example::

            {
                "playabilityStatus": {
                    "status": "OK",
                    "playableInEmbed": true,
                    "audioOnlyPlayability": {
                        "audioOnlyPlayabilityRenderer": {
                            "trackingParams": "CAEQx2kiEwiuv9X5i5H1AhWBvlUKHRoZAHk=",
                            "audioOnlyAvailability": "FEATURE_AVAILABILITY_ALLOWED"
                        }
                    },
                    "miniplayer": {
                        "miniplayerRenderer": {
                            "playbackMode": "PLAYBACK_MODE_ALLOW"
                        }
                    },
                    "contextParams": "Q0FBU0FnZ0M="
                },
                "streamingData": {
                    "expiresInSeconds": "21540",
                    "adaptiveFormats": [
                        {
                            "itag": 140,
                            "url": "https://rr1---sn-h0jelnez.c.youtube.com/videoplayback?expire=1641080272...",
                            "mimeType": "audio/mp4; codecs=\"mp4a.40.2\"",
                            "bitrate": 131007,
                            "initRange": {
                                "start": "0",
                                "end": "667"
                            },
                            "indexRange": {
                                "start": "668",
                                "end": "999"
                            },
                            "lastModified": "1620321966927796",
                            "contentLength": "3967382",
                            "quality": "tiny",
                            "projectionType": "RECTANGULAR",
                            "averageBitrate": 129547,
                            "highReplication": true,
                            "audioQuality": "AUDIO_QUALITY_MEDIUM",
                            "approxDurationMs": "245000",
                            "audioSampleRate": "44100",
                            "audioChannels": 2,
                            "loudnessDb": -1.3000002
                        }
                    ]
                },
                "playbackTracking": {
                    "videostatsPlaybackUrl": {
                      "baseUrl": "https://s.youtube.com/api/stats/playback?cl=491307275&docid=AjXQiKP5kMs&ei=Nl2HY-6MH5WE8gPjnYnoDg&fexp=1714242%2C9405963%2C23804281%2C23858057%2C23880830%2C23880833%2C23882685%2C23918597%2C23934970%2C23946420%2C23966208%2C23983296%2C23998056%2C24001373%2C24002022%2C24002025%2C24004644%2C24007246%2C24034168%2C24036947%2C24077241%2C24080738%2C24120820%2C24135310%2C24135692%2C24140247%2C24161116%2C24162919%2C24164186%2C24169501%2C24175560%2C24181174%2C24187043%2C24187377%2C24187854%2C24191629%2C24197450%2C24199724%2C24200839%2C24209349%2C24211178%2C24217535%2C24219713%2C24224266%2C24241378%2C24248091%2C24248956%2C24255543%2C24255545%2C24262346%2C24263796%2C24265426%2C24267564%2C24268142%2C24279196%2C24280220%2C24283426%2C24283493%2C24287327%2C24288045%2C24290971%2C24292955%2C24293803%2C24299747%2C24390674%2C24391018%2C24391537%2C24391709%2C24392268%2C24392363%2C24392401%2C24401557%2C24402891%2C24403794%2C24406605%2C24407200%2C24407665%2C24407914%2C24408220%2C24411766%2C24413105%2C24413820%2C24414162%2C24415866%2C24416354%2C24420756%2C24421162%2C24425861%2C24428962%2C24590921%2C39322504%2C39322574%2C39322694%2C39322707&ns=yt&plid=AAXusD4TIOMjS5N4&el=detailpage&len=246&of=Jx1iRksbq-rB9N1KSijZLQ&osid=MWU2NzBjYTI%3AAOeUNAagU8UyWDUJIki5raGHy29-60-yTA&uga=29&vm=CAEQABgEOjJBUEV3RWxUNmYzMXNMMC1MYVpCVnRZTmZWMWw1OWVZX2ZOcUtCSkphQ245VFZwOXdTQWJbQVBta0tETEpWNXI1SlNIWEJERXdHeFhXZVllNXBUemt5UHR4WWZEVzFDblFUSmdla3BKX2R0dXk3bzFORWNBZmU5YmpYZnlzb3doUE5UU0FoVGRWa0xIaXJqSWgB",
                      "headers": [
                        {
                          "headerType": "USER_AUTH"
                        },
                        {
                          "headerType": "VISITOR_ID"
                        },
                        {
                          "headerType": "PLUS_PAGE_ID"
                        }
                      ]
                    },
                    "videostatsDelayplayUrl": {(as above)},
                    "videostatsWatchtimeUrl": {(as above)},
                    "ptrackingUrl": {(as above)},
                    "qoeUrl": {(as above)},
                    "atrUrl": {(as above)},
                    "videostatsScheduledFlushWalltimeSeconds": [
                      10,
                      20,
                      30
                    ],
                    "videostatsDefaultFlushIntervalSeconds": 40
                },
                "videoDetails": {
                    "videoId": "AjXQiKP5kMs",
                    "title": "Sparks",
                    "lengthSeconds": "245",
                    "channelId": "UCvCk2zFqkCYzpnSgWfx0qOg",
                    "isOwnerViewing": false,
                    "isCrawlable": false,
                    "thumbnail": {
                        "thumbnails": []
                    },
                    "allowRatings": true,
                    "viewCount": "12",
                    "author": "Thomas Bergersen",
                    "isPrivate": true,
                    "isUnpluggedCorpus": false,
                    "musicVideoType": "MUSIC_VIDEO_TYPE_PRIVATELY_OWNED_TRACK",
                    "isLiveContent": false
                },
                "microformat": {
                    "microformatDataRenderer": {
                        "urlCanonical": "https://music.youtube.com/watch?v=AjXQiKP5kMs",
                        "title": "Sparks - YouTube Music",
                        "description": "Uploaded to YouTube via YouTube Music Sparks",
                        "thumbnail": {
                            "thumbnails": [
                                {
                                    "url": "https://i.ytimg.com/vi/AjXQiKP5kMs/hqdefault.jpg",
                                    "width": 480,
                                    "height": 360
                                }
                            ]
                        },
                        "siteName": "YouTube Music",
                        "appName": "YouTube Music",
                        "androidPackage": "com.google.android.apps.youtube.music",
                        "iosAppStoreId": "1017492454",
                        "iosAppArguments": "https://music.youtube.com/watch?v=AjXQiKP5kMs",
                        "ogType": "video.other",
                        "urlApplinksIos": "vnd.youtube.music://music.youtube.com/watch?v=AjXQiKP5kMs&feature=applinks",
                        "urlApplinksAndroid": "vnd.youtube.music://music.youtube.com/watch?v=AjXQiKP5kMs&feature=applinks",
                        "urlTwitterIos": "vnd.youtube.music://music.youtube.com/watch?v=AjXQiKP5kMs&feature=twitter-deep-link",
                        "urlTwitterAndroid": "vnd.youtube.music://music.youtube.com/watch?v=AjXQiKP5kMs&feature=twitter-deep-link",
                        "twitterCardType": "player",
                        "twitterSiteHandle": "@YouTubeMusic",
                        "schemaDotOrgType": "http://schema.org/VideoObject",
                        "noindex": true,
                        "unlisted": true,
                        "paid": false,
                        "familySafe": true,
                        "pageOwnerDetails": {
                            "name": "Music Library Uploads",
                            "externalChannelId": "UCvCk2zFqkCYzpnSgWfx0qOg",
                            "youtubeProfileUrl": "http://www.youtube.com/channel/UCvCk2zFqkCYzpnSgWfx0qOg"
                        },
                        "videoDetails": {
                            "externalVideoId": "AjXQiKP5kMs",
                            "durationSeconds": "246",
                            "durationIso8601": "PT4M6S"
                        },
                        "linkAlternates": [
                            {
                                "hrefUrl": "android-app://com.google.android.youtube/http/youtube.com/watch?v=AjXQiKP5kMs"
                            },
                            {
                                "hrefUrl": "ios-app://544007664/http/youtube.com/watch?v=AjXQiKP5kMs"
                            },
                            {
                                "hrefUrl": "https://www.youtube.com/oembed?format=json&url=https%3A%2F%2Fmusic.youtube.com%2Fwatch%3Fv%3DAjXQiKP5kMs",
                                "title": "Sparks",
                                "alternateType": "application/json+oembed"
                            },
                            {
                                "hrefUrl": "https://www.youtube.com/oembed?format=xml&url=https%3A%2F%2Fmusic.youtube.com%2Fwatch%3Fv%3DAjXQiKP5kMs",
                                "title": "Sparks",
                                "alternateType": "text/xml+oembed"
                            }
                        ],
                        "viewCount": "12",
                        "publishDate": "1969-12-31",
                        "category": "Music",
                        "uploadDate": "1969-12-31"
                    }
                }
            }

        """
        endpoint = 'player'
        if not signatureTimestamp:
            signatureTimestamp = get_datestamp() - 1

        params = {
            "playbackContext": {
                "contentPlaybackContext": {
                    "signatureTimestamp": signatureTimestamp
                }
            },
            "video_id": videoId
        }
        response = self._send_request(endpoint, params)
        keys = [
            'videoDetails', 'playabilityStatus', 'streamingData', 'microformat', 'playbackTracking'
        ]
        for k in list(response.keys()):
            if k not in keys:
                del response[k]
        return response

    def get_song_related(self, browseId: str):
        """
        Gets related content for a song. Equivalent to the content
        shown in the "Related" tab of the watch panel.

        :param browseId: The `related` key  in the `get_watch_playlist` response.

        Example::

            [
              {
                "title": "You might also like",
                "contents": [
                  {
                    "title": "High And Dry",
                    "videoId": "7fv84nPfTH0",
                    "artists": [{
                        "name": "Radiohead",
                        "id": "UCr_iyUANcn9OX_yy9piYoLw"
                      }],
                    "thumbnails": [
                      {
                        "url": "https://lh3.googleusercontent.com/TWWT47cHLv3yAugk4h9eOzQ46FHmXc_g-KmBVy2d4sbg_F-Gv6xrPglztRVzp8D_l-yzOnvh-QToM8s=w60-h60-l90-rj",
                        "width": 60,
                        "height": 60
                      }
                    ],
                    "isExplicit": false,
                    "album": {
                      "name": "The Bends",
                      "id": "MPREb_xsmDKhqhQrG"
                    }
                  }
                ]
              },
              {
                "title": "Recommended playlists",
                "contents": [
                  {
                    "title": "'90s Alternative Rock Hits",
                    "playlistId": "RDCLAK5uy_m_h-nx7OCFaq9AlyXv78lG0AuloqW_NUA",
                    "thumbnails": [...],
                    "description": "Playlist • YouTube Music"
                  }
                ]
              },
              {
                "title": "Similar artists",
                "contents": [
                  {
                    "title": "Noel Gallagher",
                    "browseId": "UCu7yYcX_wIZgG9azR3PqrxA",
                    "subscribers": "302K",
                    "thumbnails": [...]
                  }
                ]
              },
              {
                "title": "Oasis",
                "contents": [
                  {
                    "title": "Shakermaker",
                    "year": "2014",
                    "browseId": "MPREb_WNGQWp5czjD",
                    "thumbnails": [...]
                  }
                ]
              },
              {
                "title": "About the artist",
                "contents": "Oasis were a rock band consisting of Liam Gallagher, Paul ... (full description shortened for documentation)"
              }
            ]
        """
        raise_get_song(browseId)

        response = self._send_request('browse', {'browseId': browseId})
        sections = nav(response, ['contents'] + SECTION_LIST)
        return self.parser.parse_mixed_content(sections)

    def get_lyrics(self, browseId: str) -> Dict:
        """
        Returns lyrics of a song or video.

        :param browseId: Lyrics browse id obtained from `get_watch_playlist`
        :return: Dictionary with song lyrics.

        Example::

            {
                "lyrics": "Today is gonna be the day\\nThat they're gonna throw it back to you\\n",
                "source": "Source: LyricFind"
            }

        """
        lyrics = {}
        raise_get_lyrics(browseId)

        response = self._send_request('browse', {'browseId': browseId})
        lyrics['lyrics'] = nav(response,
                               ['contents'] + SECTION_LIST_ITEM + DESCRIPTION_SHELF + DESCRIPTION,
                               True)
        lyrics['source'] = nav(response, ['contents'] + SECTION_LIST_ITEM + DESCRIPTION_SHELF
                               + ['footer'] + RUN_TEXT, True)

        return lyrics

    def get_basejs_url(self):
        """
        Extract the URL for the `base.js` script from YouTube Music.

        :return: URL to `base.js`
        """
        response = self._send_get_request(url=YTM_DOMAIN)
        match = re.search(r'jsUrl"\s*:\s*"([^"]+)"', response)
        raise_match(match)

        return YTM_DOMAIN + match.group(1)

    def get_signatureTimestamp(self, url: str = None) -> int:
        """
        Fetch the `base.js` script from YouTube Music and parse out the
        `signatureTimestamp` for use with :py:func:`get_song`.

        :param url: Optional. Provide the URL of the `base.js` script. If this
            isn't specified a call will be made to :py:func:`get_basejs_url`.
        :return: `signatureTimestamp` string
        """
        if url is None:
            url = self.get_basejs_url()
        response = self._send_get_request(url=url)
        match = re.search(r"signatureTimestamp[:=](\d+)", response)
        raise_match_signature(match)

        return int(match.group(1))

    def get_tasteprofile(self) -> Dict:
        """
        Fetches suggested artists from taste profile (music.youtube.com/tasteprofile).
        Tasteprofile allows users to pick artists to update their recommendations.
        Only returns a list of suggested artists, not the actual list of selected entries

        :return: Dictionary with artist and their selection & impression value

        Example::

            {
                "Drake": {
                    "selectionValue": "tastebuilder_selection=/m/05mt_q"
                    "impressionValue": "tastebuilder_impression=/m/05mt_q"
                }
            }

        """

        response = self._send_request('browse', {'browseId': "FEmusic_tastebuilder"})
        profiles = nav(response, TASTE_PROFILE_ITEMS)

        taste_profiles = {}
        for itemList in profiles:
            for item in itemList["tastebuilderItemListRenderer"]["contents"]:
                artist = nav(item["tastebuilderItemRenderer"], TASTE_PROFILE_ARTIST)[0]["text"]
                taste_profiles[artist] = {
                    "selectionValue": item["tastebuilderItemRenderer"]["selectionFormValue"],
                    "impressionValue": item["tastebuilderItemRenderer"]["impressionFormValue"]
                }
        return taste_profiles

    def set_tasteprofile(self, artists: List[str], taste_profile: Dict = None) -> None:
        """
        Favorites artists to see more recommendations from the artist.
        Use get_tasteprofile() to see which artists are available to be recommended

        :param artists: A List with names of artists, must be contained in the tasteprofile
        :param taste_profile: tasteprofile result from :py:func:`get_tasteprofile`.
            Pass this if you call :py:func:`get_tasteprofile` anyway to save an extra request.
        :return None if successful
        """

        if taste_profile is None:
            taste_profile = self.get_tasteprofile()
        formData = {
            "impressionValues":
            [taste_profile[profile]["impressionValue"] for profile in taste_profile],
            "selectedValues": []
        }

        for artist in artists:
            if artist not in taste_profile:
                raise Exception("The artist, {}, was not present in taste!".format(artist))
            formData["selectedValues"].append(taste_profile[artist]["selectionValue"])

        body = {'browseId': "FEmusic_home", "formData": formData}
        self._send_request('browse', body)
