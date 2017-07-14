from datetime import datetime
import os
import time

from psn_api.Auth import Auth
from psn_api.Friend import Friend
from psn_api.User import User
from psn_api.Messaging import Messaging

PSN_USERNAME = os.environ['PSN_USERNAME']
PSN_PASSWORD = os.environ['PSN_PASSWORD']

def current_time():
    return datetime.utcnow().isoformat()

def do_check():
    auth = Auth(PSN_USERNAME, PSN_PASSWORD)
    tokens = auth.get_tokens()

    friend = Friend(tokens)
    online_friends = friend.my_friends(filter='online')['profiles']

    print(current_time())
    print('%s friends online' % len(online_friends))

    for profile in online_friends:
        friend = profile['onlineId']
        status = profile['primaryOnlineStatus']
        game = profile['presences'][0].get('titleName', '<nothing>')
        platform = profile['presences'][0].get('platform', '<unknown>')
        print('[{platform}] {friend} is {status}, playing {game}'.format(
            platform=platform,
            friend=friend,
            status=status,
            game=game,
        ))


if __name__ == '__main__':
    do_check()
