import time
import os

from check import do_check, get_auth

# This interval is how often to query psn
INTERVAL = int(os.environ['PSN_CHECK_INTERVAL'])

TOKEN_REFRESH_INTERVAL = os.environ.get('TOKEN_REFRESH_INTERVAL', 3500)

# We'll wake up more often than INTERVAL and check if we have work to do
WAKEUP_INTERVAL = 5


def main():
    auth = get_auth()
    tokens = auth.get_tokens()

    next_token_refresh = time.time() + TOKEN_REFRESH_INTERVAL
    next_wake_up = -1

    print('heroku_start.py - main()')
    while True:
        if time.time() >= next_token_refresh:
            if not auth.refreshTokens():
                print("Failed to refresh tokens - quitting")
                return

            tokens = auth.get_tokens()
            next_token_refresh = time.time() + TOKEN_REFRESH_INTERVAL

        if time.time() >= next_wake_up:
            do_check(tokens)
            next_wake_up = time.time() + INTERVAL

        time.sleep(WAKEUP_INTERVAL)

if __name__ == '__main__':
    main()
