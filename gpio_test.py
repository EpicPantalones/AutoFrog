import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define the pins to be tested
pins = [11, 12, 13, 15, 16, 18, 22, 29]

# Setup the pins as outputs
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Loop through the pins and toggle them ON and OFF
for pin in pins:
    GPIO.output(pin, GPIO.HIGH)
    print(f"Pin {pin} ON")

time.sleep(120)

# Loop through the pins and toggle them ON and OFF
for pin in pins:
    GPIO.output(pin, GPIO.LOW)
    print(f"Pin {pin} OFF")

# Clean up GPIO settings
GPIO.cleanup()
