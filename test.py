import unittest
import json

import mock
import requests
import requests_mock

from psn.cli import format_friend_status_message
from psn import client

profile  = {
    u'avatarUrls': [
        {
            u'avatarUrl': u'http://some-url.com/avatar.png',
            u'size': u'l',
        },
    ],
    u'following': False,
    u'friendRelation': u'friend',
    u'isOfficiallyVerified': False,
    u'onlineId': u'wumbo-online-id\xae',
    u'personalDetail': {
        u'firstName': u'Patrick',
        u'lastName': u'Star',
    },
    u'personalDetailSharing': u'shared',
    u'plus': 1,
    u'presences': [{
        u'hasBroadcastData': False,
        u'npTitleIconUrl': u'http://some-url/icon0.png',
        u'npTitleId': u'some-title-id',
        u'onlineStatus': u'online\xae',
        u'platform': u'PS4\xae',
        u'titleName': u'Rocket League\xae'
    }],
    u'primaryOnlineStatus': u'online',
    u'trophySummary': {u'level': 4}
}


class TestUnicode(unittest.TestCase):
    """Some tests to check for successful handling of unicode data"""

    def test_format_friend_status_message(self):
        format_friend_status_message(profile)

    def test_do_request(self):
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock', adapter)

        adapter.register_uri('GET', 'mock://test-unicode',
                             text=u'Rocket League\xae')

        client.requests = session
        client.do_request('GET', 'mock://test-unicode')

if __name__ == '__main__':
    unittest.main(verbosity=2)
