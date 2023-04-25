from lib.remote.tx import TX
from lib.remote.tx.get_pin import pin
from machine import Pin
import time
import utime
import uasyncio as asyncio


debounce_time = 0
button = Pin(5, Pin.IN, Pin.PULL_DOWN)
led = Pin("LED", Pin.OUT)

def callback(button):
    global  debounce_time
    if (time.ticks_ms() - debounce_time) > 500:
        for _ in range(10):
            transmit('trigger')
            await asyncio.sleep_ms(delay)
        debounce_time = time.ticks_ms()

button.irq(trigger=Pin.IRQ_RISING, handler=callback)

transmit = TX(pin(),fname='triggers', reps=10)

delay = transmit.latency()

while True:
    pass
