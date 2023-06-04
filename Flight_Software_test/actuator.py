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