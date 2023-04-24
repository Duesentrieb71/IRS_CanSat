from lib.remote.rx import RX
from lib.remote.rx.get_pin import pin
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

recv = RX(pin())

#pairing (receiving a signal from the transmitter and storing it with the specified name) using recv('on')

def pair(key):
    recv(key)

    starttime = time.ticks_ms()
    while time.ticks_ms() - starttime < 500:
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.1)
        
    time.delay(5)
    recv.save('remotes')
    

while True:
    if interrupt_flag == 1:
        interrupt_flag = 0
        pair('on')

        
