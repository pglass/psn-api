from src.Auth import Auth
from src.Friend import Friend
from src.User import User
from src.Messaging import Messaging

import logging
logging.basicConfig(level=logging.DEBUG)

auth = Auth('poo', 'wumbo')
tokens = auth.get_tokens()

friend = Friend(tokens)
online_friends = friend.my_friends(filter='online')['profiles']
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
