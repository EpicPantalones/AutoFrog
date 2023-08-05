import RPi.GPIO as GPIO
from enum import IntEnum
import signal
import time

'''
This IntEnum contains the pin number that should be used for each
channel. Change them here, and the entire rest of the program changes.
Pins can also be individually addressed with "C.NUM"
'''
class C(IntEnum):
    ONE = 11
    TWO = 12
    THREE = 13
    FOUR = 15
    FIVE = 16
    SIX = 18
    SEVEN = 22
    EIGHT = 29
    
'''
A refence list that can be used to iterate through pins;
calling CHAN[#] will return the correct pin number.
'''
CHAN = [C.ONE, C.TWO, C.THREE, C.FOUR, C.FIVE, C.SIX, C.SEVEN, C.EIGHT]
            
'''
function for setting pins
for state - True is on, False is off
'''
def set_pin(pin,state):
    assert state in [True,False], f"{state} is not a valid state."
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

'''
test function - will blink the lights on
and off for "count" times
'''
def blinker(count):
    for i in range(0,count):
        for pin in CHAN:
            set_pin(pin,True)
            print(f"Pin {pin} ON")
        time.sleep(5)
        for pin in CHAN:
            set_pin(pin,False)
            print(f"Pin {pin} OFF")

'''
init function for controlling the setup of the board when program is first run.
This should handle all the setup for the program and loading in things from files
etc. It should also load the server thread that listens for incoming commands.
'''
def init():
    # Set the GPIO mode
    GPIO.setmode(GPIO.BOARD)
    for pin in CHAN:
                GPIO.setup(pin, GPIO.OUT)
    # Load in the default states
    
    # Load in the config
    
    # Start the server thread

'''
This should run until interrupted. The server thread should 
call here for interrupts?
'''
def loop():
    return

'''
What to do if the program is allowed to exit cleanly (Ctrl+C only)
'''
def signal_handler(sig, frame):
    GPIO.cleanup()
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    init()
    loop()
    
