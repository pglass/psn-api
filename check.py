import json
from datetime import datetime
import os
import time

import requests

from psn_api.Auth import Auth
from psn_api.Friend import Friend
from psn_api.User import User
from psn_api.Messaging import Messaging

PSN_USERNAME = os.environ['PSN_USERNAME']
PSN_PASSWORD = os.environ['PSN_PASSWORD']

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
NOTIFY_USERS = os.environ.get('NOTIFY_USERS')

def current_time():
    return datetime.utcnow().isoformat()

def should_notify_user(profile):
    if not NOTIFY_USERS:
        return True
    user = profile['onlineId']
    game = profile['presences'][0].get('titleName')
    return game and user in NOTIFY_USERS

def get_auth():
     return Auth(PSN_USERNAME, PSN_PASSWORD)

def do_check(tokens):
    friend = Friend(tokens)
    online_friends = friend.my_friends(filter='online')['profiles']

    print(current_time())
    print('%s friends online' % len(online_friends))

    slack_msg = ''
    for profile in online_friends:
        friend = profile['onlineId']
        status = profile['primaryOnlineStatus']
        game = profile['presences'][0].get('titleName', '<nothing>')
        platform = profile['presences'][0].get('platform', '<unknown>')

        msg = '[{platform}] {friend} is {status}, playing {game}'.format(
            platform=platform,
            friend=friend,
            status=status,
            game=game,
        )
        print(msg)
        if SLACK_WEBHOOK_URL and should_notify_user(profile):
            slack_msg += msg + '\n'

    if not SLACK_WEBHOOK_URL:
        print('(no slack hook url)')
    elif SLACK_WEBHOOK_URL and slack_msg:
        resp = requests.post(SLACK_WEBHOOK_URL,
                             data=json.dumps({"text": slack_msg}))
        if not resp.ok:
            print('[%s] Failed to send slack msg: %s'
                  % (resp.status_code, resp.text))
        else:
            print('[%s] Sent slack msg' % resp.status_code)

if __name__ == '__main__':
    do_check(get_auth().get_tokens())
