# Send morse code over serial USB connection via print
# Designed for Gemma M0

from digitalio import DigitalInOut, Direction
from touchio import TouchIn
import adafruit_dotstar as dotstar
import board
import time

BRIGHTNESS = 0.2

# Show green while accepting input
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot[0] = (0, 255, 0)
dot.brightness = BRIGHTNESS
dot.show()

# Use built in red LED to display touch feedback
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Capacitive touch
touch0 = TouchIn(board.A0)
touch1 = TouchIn(board.A1)
touch2 = TouchIn(board.A2)

# based on experimentation. anything less than 600 loops is a '.', anything more is a '-'
dash_length = 600

i = 0
touching = False  # keep state between loops
letter_buffer = []

while True:
    led.value = touch2.value
    i += 1

    # send tweet
    if touching and touch2.value:
        if i > dash_length * 10:
            print('EOF')
            touching = False
            i = 0
            dot.brightness = 0
            dot.show()
            time.sleep(2)
            dot.brightness = BRIGHTNESS
            dot.show()

    # has the state changed?
    if touching and not touch2.value:
        # we just stopped touching it
        # read how long it was touched 
        if 5 < i < dash_length:
            letter_buffer.append('.')
        elif i >= dash_length:
            letter_buffer.append('-')
        touching = False
        i = 0

    if not touching and touch2.value:
        # we just started touching it
        touching = True
        i = 0

    if not touching and not touch2.value:
        if touch0.value:
            print('BACK')
            # turn light off while not receiving input
            dot.brightness = 0
            dot.show()
            time.sleep(0.5)
            dot.brightness = BRIGHTNESS
            dot.show()
        elif touch1.value:
            print('SPACE')
            dot.brightness = 0
            dot.show()
            time.sleep(0.5)
            dot.brightness = BRIGHTNESS
            dot.show()
        elif i > dash_length and letter_buffer:
            # we found a full character!
            letter = ''.join(letter_buffer)
            print(letter)
            letter_buffer = []
