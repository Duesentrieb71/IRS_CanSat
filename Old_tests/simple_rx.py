# Script to receive a trigger signal

import machine
import time
import utime

# Set up GPIO pins
pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Receive trigger signal
starttime = utime.ticks_ms()

interval_times = [0, 0, 0, 0, 0]

while True:
    if pin.value() == 1:
        #print('Trigger signal received')
        last_trigger = utime.ticks_diff(utime.ticks_ms(), starttime)
        for i in range(4):
            interval_times[i] = interval_times[i+1] #push the interval times list up one

        interval_times[4] = last_trigger #update the last interval time

        print(last_trigger, "ms since last trigger")
        #if all interval times are between 202 and 198 ms, we have a valid trigger
        if all(198 <= x <= 202 for x in interval_times):
            print("Valid trigger")
            print(interval_times)
        else:
            print("Invalid trigger")
            print(interval_times)
        starttime = utime.ticks_ms()
        time.sleep(0.08)

