import time
import uasyncio as asyncio # Using async from MicroPython
from lib.ibus import IBus

global ibus_in
global released

def initialize():
    global ibus_in
    global released
    released = False
    ibus_in = IBus(1, 115200, 10)

async def release_CanSat():
    print("\nReleasing CanSat in")
    for i in range(5, 0, -1):
        print(i)
        await asyncio.sleep(1)
    print("good luck!")
    global released
    released = True

async def get_status():
    while not released:
        res = ibus_in.read()
        # if signal then display immediately
        if (res[0] == 1):
            if (IBus.normalize(res[8]) > 50):
                asyncio.create_task(release_CanSat())
            print(" - {}".format(time.ticks_ms()))
        else:
            print ("Status offline {}".format(res[0]))
        await asyncio.sleep(0.5)


