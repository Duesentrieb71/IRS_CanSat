from lib.remote.tx import TX
from lib.remote.tx.get_pin import pin
from machine import Pin
import time
import utime
import uasyncio as asyncio

debounce_time = 0

transmit = TX(pin(),fname='triggers', reps=10)

delay = transmit.latency()

led = Pin(1, Pin.OUT)

button = Pin(5, Pin.IN, Pin.PULL_DOWN)

def blink(delay, reps=5):
    for _ in range(2*reps):
        led.toggle()
        time.sleep(delay)

def callback(button):
    global debounce_time
    if utime.ticks_ms() - debounce_time > 500:
        blink(0.05)
        for _ in range(10):
            blink(0.1, 1)
            transmit('trigger')
            #await asyncio.sleep_ms(delay)
            time.sleep(delay/1000)
        debounce_time = utime.ticks_ms()
        
button.irq(trigger=Pin.IRQ_RISING, handler=callback)

while True:
    print(utime.ticks_ms())
