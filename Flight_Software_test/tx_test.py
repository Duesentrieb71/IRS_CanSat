from lib.remote.tx import TX
from lib.remote.tx.get_pin import pin
from machine import Pin
import time

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

transmit = TX(pin(), reps=10)