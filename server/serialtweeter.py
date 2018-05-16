#!/usr/bin/env python3

import datetime
import json
import serial
import sys
from tweepy import API, OAuthHandler

with open('creds.json', 'r') as f:
    creds = json.loads(f.read())

ck = creds['consumer_key']
cs = creds['consumer_secret']
ak = creds['access_key']
acs = creds['access_secret']

auth = OAuthHandler(ck, cs)
auth.set_access_token(ak, acs)

api = API(auth)

s = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout=1)

print('Listening... <Ctrl+C> to exit')

# Show underscores instead of spaces while constructing message
def print_buffer(message_buffer):
    return ''.join('_' if x == ' ' else x for x in message_buffer)

def main():
    message_buffer = []
    control_characters = ('EOF', 'BACK')

    while True:
        char = s.readline().decode('utf-8').strip()
        if len(char) > 10:
            # catch and ignore messages that come from reloading code on the Gemma
            continue

        if message_buffer and char == 'EOF':
            api.update_status(status=''.join(message_buffer) + " #pycon2018 #morsecodetweet")
            print('Tweeted', ''.join(message_buffer))
            message_buffer = []
        elif message_buffer and char == 'BACK':
            message_buffer.pop()
            print('Message:', print_buffer(message_buffer))
        elif char and char not in control_characters:
            if char == 'SPACE':
                char = ' '
            message_buffer.append(char)
            print('Message:', print_buffer(message_buffer))

if __name__ == '__main__':
    try:
        main()
    # Quit nicely instead of printing stacktrace
    except KeyboardInterrupt:
        print()
        print('Bye!')
        sys.exit(0)
