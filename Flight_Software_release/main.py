import comms
import time
import uasyncio as asyncio # Using async from MicroPython

comms.initialize()

async def main():
    asyncio.create_task(comms.get_status())

if __name__ == "__main__":
    asyncio.run(main())

    