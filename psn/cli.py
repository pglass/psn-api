import argparse
import json
import logging
from datetime import datetime
import os
import time

import requests

from psn.auth import Auth
from psn.api import PSN

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
NOTIFY_USERS = os.environ.get('NOTIFY_USERS')

# How often to query the friends list
PSN_CHECK_INTERVAL = int(os.environ.get('PSN_CHECK_INTERVAL') or 600)
# How often to refresh tokens
TOKEN_REFRESH_INTERVAL = int(os.environ.get('TOKEN_REFRESH_INTERVAL') or 3500)
# How often to wake up and check for work
WAKEUP_INTERVAL = int(os.environ.get('WAKEUP_INTERVAL') or 60)

def current_time():
    return datetime.utcnow().isoformat()

def should_notify_user(profile):
    if not NOTIFY_USERS:
        return True
    user = profile['onlineId']
    game = profile['presences'][0].get('titleName')
    return game and user in NOTIFY_USERS

def send_slack_msg(msg):
    if not SLACK_WEBHOOK_URL or not msg:
        return

    resp = requests.post(SLACK_WEBHOOK_URL,
                         data=json.dumps({"text": msg}))
    if not resp.ok:
        print('[%s] Failed to send slack msg: %s'
              % (resp.status_code, resp.text))
    else:
        print('[%s] Sent slack msg' % resp.status_code)


def format_friend_status_message(profile):
    friend = profile['onlineId']
    status = profile['primaryOnlineStatus']
    game = profile['presences'][0].get('titleName', '<nothing>')
    platform = profile['presences'][0].get('platform', '<unknown>')

    return u'[{platform}] {friend} is {status}, playing {game}'.format(
        platform=platform,
        friend=friend,
        status=status,
        game=game,
    )


def do_check(psn):
    online_friends = psn.my_friends(filter='online')['profiles']

    print(current_time())
    print('%s friends online' % len(online_friends))

    slack_msg = ''
    for profile in online_friends:
        msg = format_friend_status_message(profile)
        print(msg)
        if SLACK_WEBHOOK_URL and should_notify_user(profile):
            slack_msg += msg + '\n'

    send_slack_msg(slack_msg)

def loop(psn):
    msg = 'Looping forever...'
    msg += '\nPSN_CHECK_INTERVAL = %s' % PSN_CHECK_INTERVAL
    msg += '\nTOKEN_REFRESH_INTERVAL = %s' % TOKEN_REFRESH_INTERVAL
    msg += '\nWAKEUP_INTERVAL = %s' % WAKEUP_INTERVAL
    msg += '\nNOTIFY_USERS = %s' % NOTIFY_USERS
    msg += '\nSLACK_WEBHOOK_URL = %s' % (
        '<set>' if SLACK_WEBHOOK_URL else '<not-set>'
    )

    print msg
    send_slack_msg(msg)

    next_token_refresh = time.time() + TOKEN_REFRESH_INTERVAL
    next_wake_up = -1
    while True:
        if time.time() >= next_token_refresh:
            psn.auth.refresh_login()
            next_token_refresh = time.time() + TOKEN_REFRESH_INTERVAL

        if time.time() >= next_wake_up:
            do_check(psn)
            next_wake_up = time.time() + PSN_CHECK_INTERVAL

        time.sleep(WAKEUP_INTERVAL)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-1', '--once', action='store_true')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    psn = PSN(Auth())
    if args.once:
        do_check(psn)
    else:
        loop(psn)

if __name__ == '__main__':
    main()
