import os

from psn import config
from psn import payloads
from psn.client import do_request


class AuthError(Exception): pass


class Auth(object):

    def __init__(self, username=None, password=None):
        self.username = username or os.environ['PSN_USERNAME']
        self.password = password or os.environ['PSN_PASSWORD']

        self.npsso = None
        self.grant_code = None
        self.access_token = None
        self.refresh_token = None

        self.login()

    def login(self):
        self.npsso = self._get_npsso()
        self.grant_code = self._get_grant_code(self.npsso)

        tokens = self._get_oauth_tokens(self.grant_code)
        self.access_token, self.refresh_token = tokens

    def refresh_login(self):
        if not self.refresh_token:
            self.login()
            return

        payload = payloads.get_refresh_payload(self.refresh_token)
        resp = do_request('POST', config.OAUTH_URL, data=payload)
        try:
            self.access_token = resp.json()['access_token']
            self.refresh_token = resp.json()['refresh_token']
        except:
            raise AuthError("Failed refresh oauth tokens")

    def _get_npsso(self):
        payload = payloads.get_login_payload(self.username, self.password)
        resp = do_request('POST', config.SSO_URL, data=payload)
        try:
            return resp.json()['npsso']
        except:
            raise AuthError("Failed to get npsso")

    def _get_grant_code(self, npsso):
        resp = do_request('GET', config.CODE_URL, params=payloads.CODE_PAYLOAD,
                          headers={'Cookie': 'npsso=%s' % npsso})
        try:
            return resp.headers['X-NP-GRANT-CODE']
        except:
            raise AuthError("Failed to get grant code")

    def _get_oauth_tokens(self, grant_code):
        payload = payloads.get_oauth_payload(grant_code)
        resp = do_request('POST', config.OAUTH_URL, data=payload)
        try:
            return resp.json()['access_token'], resp.json()['refresh_token']
        except:
            raise AuthError("Failed get oauth tokens")

    @property
    def authorization_headers(self):
        return {
            'Authorization': 'Bearer %s' % self.access_token,
        }
