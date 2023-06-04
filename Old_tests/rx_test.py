from lib.remote.rx import RX
from lib.remote.rx.get_pin import pin
from machine import Pin
import time

led = Pin(1, Pin.OUT)

recv = RX(pin())

def blink(delay, reps=5):
    for _ in range(2*reps):
        led.toggle()
        time.sleep(delay)


while True: # wait for trigger signal from ground station
    blink(0.05)
    recv.load('triggers_tmp')
    recv('trigger')
    recv.save('triggers_tmp')
    triggers = open ('triggers', 'r')
    triggers_tmp = open ('triggers_tmp', 'r')
    if triggers.read() == triggers_tmp.read():
        blink(0.5, 10)
        break
    triggers.close()
    triggers_tmp.close()
    with open ('triggers_tmp', 'w') as f:
        f.write("{"+"}")


### drop CanSat ###
print('drop CanSat')

