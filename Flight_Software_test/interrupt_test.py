from machine import Pin
import time
import utime

debounce_time = utime.ticks_ms()

led = Pin(1, Pin.OUT)

#button pin interrupt

button = Pin(5, Pin.IN, Pin.PULL_DOWN)

def callback(button):
    global debounce_time
    if utime.ticks_ms() - debounce_time > 500:
        for _ in range(10):
            led.toggle()
            time.sleep(0.1)
        debounce_time = utime.ticks_ms()
        
button.irq(trigger=Pin.IRQ_RISING, handler=callback)

while True:
    print(utime.ticks_ms())

