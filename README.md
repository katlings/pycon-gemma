# pycon-gemma

Turning taps into tweets since PyCon 2018

Running at [@pycon_gemma](https://twitter.com/pycon_gemma)

## Setup

Required:
* A Gemma M0 board with [CircuitPython](https://github.com/adafruit/circuitpython)
* USB connection to a computer
* Twitter app credentials (via [apps.twitter.com](https://apps.twitter.com/))

### Board setup

Plug the Gemma board in via USB and copy [the board file](gemma/main.py) over. See [CircuitPython tutorials](https://learn.adafruit.com/welcome-to-circuitpython) for help connecting to the board and updating files.

### Server setup

With the API key you generated via apps.twitter.com, store access tokens in a new file `server/creds.json`.

```
{
    "consumer_key": "www",
    "consumer_secret": "xxx",
    "access_key": "yyy",
    "access_secret": "zzz"
}
```

Install the packages in [requirements.txt](requirements.txt) and run with `./server/serialtweeter.py`. Tested with Python 3.6.5.

## Usage

Input is read via capacitive touch plates on the Gemma.

```
                     ______
                    /o    o\
backspace (A0) ->  |o  M0  o|  <- (A2) tap! / hold to tweet (~5 sec)
                    \o_--_o/  <- (A1) insert space
    USB connection ->  ||
```

The board reads one character at a time and sends it over the USB connection to the server, which displays
the message that has been collected so far. Once the message is complete, long-press the 'tap' plate to send a tweet!
