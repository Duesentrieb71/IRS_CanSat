#responsible for controlling the actuators which release the payload and the parachute
from machine import Pin
import time
import uasyncio # Using async from MicroPython


async def release_CanSat():
    print("\nReleasing CanSat in")
    for i in range(5, 0, -1):
        print(i)
        await uasyncio.sleep(1)
    print("good luck!")

async def blink_LED():
    led = Pin(25, Pin.OUT)
    for i in range(10):
        led.value(not led.value())
        await uasyncio.sleep(0.5)