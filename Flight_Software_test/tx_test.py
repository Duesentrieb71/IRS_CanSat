from lib.remote.tx import TX
from lib.remote.tx.get_pin import pin
from machine import Pin
import time
import utime
import uasyncio as asyncio

interrupt_flag = 0
debounce_time = 0
button = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

def callback(button):
    global interrupt_flag, debounce_time
    if (time.ticks_ms() - debounce_time) > 500:
        interrupt_flag = 1
        debounce_time = time.ticks_ms()

button.irq(trigger=Pin.IRQ_FALLING, handler=callback)

transmit = TX(pin(),fname='trigger_key', reps=10)

delay = transmit.latency()

while True: #trigger the transmitter by pressing the button
    if interrupt_flag == 1:
        interrupt_flag = 0
        starttime_ms = utime.ticks_ms()
        for _ in range(10):
            transmit('trigger')
            await asyncio.sleep_ms(delay)
