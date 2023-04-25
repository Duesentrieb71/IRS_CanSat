from lib.remote.rx import RX
from lib.remote.rx.get_pin import pin
from machine import Pin
import time

led = Pin(1, Pin.OUT)

recv = RX(pin())


while True: # wait for trigger signal from ground station
    led.value(1)
    time.sleep(1)
    led.value(0)
    recv.load('triggers_tmp')
    recv('trigger')
    recv.save('triggers_tmp')
    triggers = open ('triggers', 'r')
    triggers_tmp = open ('triggers_tmp', 'r')
    if triggers.read() == triggers_tmp.read():
        led.value(1)
        time.sleep(3)
        led.value(0)
        break
    triggers.close()
    triggers_tmp.close()
    with open ('triggers_tmp', 'w') as f:
        f.write("{"+"}")


### drop CanSat ###
print('drop CanSat')

