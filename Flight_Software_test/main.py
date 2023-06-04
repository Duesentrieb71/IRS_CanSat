import comms
import sensor_data
import uasyncio # Using async from MicroPython

released = False

async def main():
    task_get_status = uasyncio.create_task(comms.get_status())
    task_get_data = uasyncio.create_task(sensor_data.get_data())
    await uasyncio.gather(task_get_status, task_get_data)

    print("done")


if __name__ == "__main__":
    uasyncio.run(main())