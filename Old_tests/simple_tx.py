# Script to send a trigger signal

import machine
import time

# Set up GPIO pins
pin = machine.Pin(17, machine.Pin.OUT)

# Send trigger signal
while True:
    pin.on()
    print("on")
    time.sleep(0.3)
    pin.off()
    print("off")
    time.sleep(0.3)
