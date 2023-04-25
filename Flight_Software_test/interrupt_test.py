from machine import Pin
import time
import utime

starttime_ms = utime.ticks_ms()

led = Pin(1, Pin.OUT)

#button pin interrupt

button = Pin(5, Pin.IN, Pin.PULL_DOWN)

def callback(button):
    global starttime_ms
    if utime.ticks_ms() - starttime_ms > 500:
        for _ in range(10):
            led.toggle()
            time.sleep(0.1)
        starttime_ms = utime.ticks_ms()
        
button.irq(trigger=Pin.IRQ_RISING, handler=callback)

while True:
    print(utime.ticks_ms())

