from psn import config

LOGIN_PAYLOAD = {
    "authentication_type": 'password',
    "username": None,
    'password': None,
    'client_id': config.LOGIN_CLIENT_ID,
}

OAUTH_PAYLOAD = {
    "app_context": "inapp_ios",
    "client_id": config.OAUTH_CLIENT_ID,
    "client_secret": config.OAUTH_CLIENT_SECRET,
    "code": None,
    "duid": config.DUID,
    "grant_type": "authorization_code",
    "scope": config.SCOPE,
}

CODE_PAYLOAD = {
    "state": "06d7AuZpOmJAwYYOWmVU63OMY",
    "duid": config.DUID,
    "app_context": "inapp_ios",
    "client_id": config.OAUTH_CLIENT_ID,
    "scope": config.SCOPE,
    "response_type": "code"
}

REFRESH_OAUTH_PAYLOAD = {
    "app_context": "inapp_ios",
    "client_id": config.OAUTH_CLIENT_ID,
    "client_secret": config.OAUTH_CLIENT_SECRET,
    "refresh_token": None,
    "duid": config.DUID,
    "grant_type": "refresh_token",
    "scope": config.SCOPE,
}

def get_login_payload(username, password):
    result = dict(LOGIN_PAYLOAD)
    result['username'] = username
    result['password'] = password
    return result

def get_oauth_payload(grant_code):
    result = dict(OAUTH_PAYLOAD)
    result['code'] = grant_code
    return result

def get_refresh_payload(refresh_token):
    result = dict(REFRESH_OAUTH_PAYLOAD)
    result['refresh_token'] = refresh_token
    return result
