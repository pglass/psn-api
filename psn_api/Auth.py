from .client import do_request


class Auth:

    oauth = None
    npsso = None
    grant_code = None
    refresh_token = None

    SSO_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/ssocookie'
    CODE_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize'
    OAUTH_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token'


    login_request = {
                        "authentication_type": 'password',
                        "username": None,
                        'password': None,
                        'client_id': '71a7beb8-f21a-47d9-a604-2e71bee24fe0'
                    }

    oauth_request = {
                        "app_context": "inapp_ios",
                        "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                        "client_secret": "zsISsjmCx85zgCJg",
                        "code": None,
                        "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
                        "grant_type": "authorization_code",
                        "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes"
                    }

    code_request = {
                        "state": "06d7AuZpOmJAwYYOWmVU63OMY",
                        "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
                        "app_context": "inapp_ios",
                        "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                        "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes",
                        "response_type": "code"
                    }

    refresh_oauth_request = {
                                "app_context": "inapp_ios",
                                "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                                "client_secret": "zsISsjmCx85zgCJg",
                                "refresh_token": None,
                                "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
                                "grant_type": "refresh_token",
                                "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes"
                            }

    two_factor_auth_request = {
                                "authentication_type": "two_step",
                                "ticket_uuid": None,
                                "code": None,
                                "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                              }

    def __init__(self, email, password, ticket='', code=''):
        self.login_request['username'] = email
        self.login_request['password'] = password
        self.two_factor_auth_request['ticket_uuid'] = ticket
        self.two_factor_auth_request['code'] = code
        if (not self.GrabNPSSO() or
                not self.GrabCode() or
                not self.GrabOAuth()):
            print('Error')


    def GrabNPSSO(self):
        if self.two_factor_auth_request['ticket_uuid'] and self.two_factor_auth_request['code']:
            # not used??
            resp = do_request('POST', self.SSO_URL, data=self.two_factor_auth_request)
            data = resp.json()
        else:
            resp = do_request('POST', self.SSO_URL, data=self.login_request)
            data = resp.json()
            if 'error' in data:
                print('Error during request to %s: %s' % (self.SSO_URL, data))
                return False
            if 'ticket_uuid' in data:
                print('Error - 2FA code required (ticket_uuid = %s)'
                      % data['ticket_uuid'])
                return False
        self.npsso = data['npsso']
        return True

    def find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def GrabCode(self):
        resp = do_request('GET', self.CODE_URL, params=self.code_request,
                          headers={'Cookie': 'npsso=%s' % self.npsso})
        self.grant_code = resp.headers.get('X-NP-GRANT-CODE')

        if not self.grant_code:
            print('Error - Failed to obtain X-NP-GRANT-CODE')
            return False

        return True

    def GrabOAuth(self):
        self.oauth_request['code'] = self.grant_code

        resp = do_request('POST', self.OAUTH_URL, data=self.oauth_request)
        data = resp.json()

        if 'error' in data:
            print('Error - Failed to grab oauth')
            return False

        self.oauth = data['access_token']
        self.refresh_token = data['refresh_token']
        return True

    def refreshTokens(self):
        print('Refreshing token')
        if self.refresh_token:
            self.refresh_oauth_request['refresh_token'] = self.refresh_token

            resp = do_request('POST', self.OAUTH_URL,
                              data=self.refresh_oauth_request)

            if not resp.ok:
                print('Error - Failed to refresh tokens')
                return False

            data = resp.json()
            self.oauth = data['access_token']
            self.refresh_token = data['refresh_token']
        else:
            print('No refresh token found - logging in again')
            if (not self.GrabNPSSO() or
                    not self.GrabCode() or
                    not self.GrabOAuth()):
                print('Error - failed to login')
                return False
        return True


    def get_tokens(self):
        tokens = {
            "oauth": self.oauth,
            "refresh": self.refresh_token,
            "npsso": self.npsso
        }

        if not all(tokens.values()):
            raise Exception("Failed to get tokens for user %r: %s"
                            % (self.login_request['username'], tokens))

        return tokens
