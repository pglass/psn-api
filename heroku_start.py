import time
import os

from check import do_check

INTERVAL = int(os.environ['PSN_CHECK_INTERVAL'])

def main():
    print('heroku_start.py - main()')
    while True:
        do_check()
        time.sleep(INTERVAL)

main()
