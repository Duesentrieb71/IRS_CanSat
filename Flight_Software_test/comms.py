import time
import uasyncio # Using async from MicroPython
from lib.ibus import IBus
import actuator

ibus_in = IBus(1, 115200, 10)

async def get_status():
    while True:
        res = ibus_in.read()
        # if signal then display immediately
        if (res[0] == 1):
            print ("Status {} Ch 8 {}".format(
                res[0],    # Status
                IBus.normalize(res[8]),
                ),
                end="")
            print(" - {}".format(time.ticks_ms()))
            if (IBus.normalize(res[8]) > 50):
                await actuator.release_CanSat()
                break
        else:
            print ("Status offline {}".format(res[0]))
        await uasyncio.sleep(0.01)

async def dummy():
    myIter = 0
    while myIter < 10:
        myIter += 1
        print("dummy")
        await uasyncio.sleep(1)

if __name__ == "__main__":
    uasyncio.run(get_status())