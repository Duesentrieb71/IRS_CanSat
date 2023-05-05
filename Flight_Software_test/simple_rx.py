# Script to receive a trigger signal

import machine
import time
import utime

# Set up GPIO pins
pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Receive trigger signal
starttime = utime.ticks_ms()
counter = 0
culmuative_trigger = 0
while True:
    if pin.value() == 1:
        counter += 1
        last_trigger = utime.ticks_diff(utime.ticks_ms(), starttime)
        culmuative_trigger = culmuative_trigger + last_trigger
        print("median time between triggers:", culmuative_trigger/counter, "ms")
        print(last_trigger, "ms since last trigger")
        starttime = utime.ticks_ms()
        print('Trigger signal received')
        time.sleep(0.1)
