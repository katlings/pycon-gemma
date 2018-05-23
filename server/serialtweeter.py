#!/usr/bin/env python3

import datetime
import json
import sys

import click
import serial
from tweepy import API, OAuthHandler

from morse import morse_code_dict


with open('creds.json', 'r') as f:
    creds = json.loads(f.read())

ck = creds['consumer_key']
cs = creds['consumer_secret']
ak = creds['access_key']
acs = creds['access_secret']

print('Listening... <Ctrl+C> to exit')

# Show underscores instead of spaces while constructing message
def print_buffer(message_buffer):
    return ''.join('_' if x == ' ' else x for x in message_buffer)


@click.command()
@click.argument('serial_port')
def main(serial_port):
    auth = OAuthHandler(ck, cs)
    auth.set_access_token(ak, acs)

    api = API(auth)

    s = serial.Serial(serial_port, 115200, timeout=1)
    message_buffer = []
    control_characters = ('EOF', 'BACK')

    while True:
        code = s.readline().decode('utf-8').strip()
        if len(code) > 10:
            # catch and ignore messages that come from reloading code on the Gemma
            continue

        # default to the .- representation if code not recognized
        letter = morse_code_dict.get(code, code)

        if message_buffer and letter == 'EOF':
            api.update_status(status=''.join(message_buffer))
            print('Tweeted', ''.join(message_buffer))
            message_buffer = []
        elif message_buffer and letter == 'BACK':
            message_buffer.pop()
            print('Message:', print_buffer(message_buffer))
        elif letter and letter not in control_characters:
            if letter == 'SPACE':
                letter = ' '
            message_buffer.append(letter)
            print('Message:', print_buffer(message_buffer))

if __name__ == '__main__':
    try:
        main()
    # Quit nicely instead of printing stacktrace
    except KeyboardInterrupt:
        print()
        print('Bye!')
        sys.exit(0)
