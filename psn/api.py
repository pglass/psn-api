import config

from psn.client import do_request


class PSN(object):

    def __init__(self, auth):
        self.auth = auth

    def my_friends(self, filter=None, limit=30,
                   fields=config.DEFAULT_FRIEND_FIELDS):
        url = config.USERS_URL + '/me/friends/profiles2'
        params = {
            "fields": ",".join(fields),
            "offset": 0,
            "limit": str(limit),
        }
        if filter:
            params['userFilter'] = filter

        resp = do_request('GET', url, headers=self.auth.authorization_headers,
                          params=params)
        return resp.json()
