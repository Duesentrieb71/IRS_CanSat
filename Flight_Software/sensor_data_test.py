from machine import I2C, Pin, SPI

from lib.csv import CSV

import uos
import utime
import time
import uasyncio


header = ['test1', 'test2', 'test3', 'test4']
csv = CSV('data.csv', header)

async def read_accel(shared_data, lock):
    while True:
        data = [time.time()]
        async with lock:
            shared_data['accel'] = data
        await uasyncio.sleep(5)

async def read_gyro(shared_data, lock):
    while True:
        data = [time.time()]
        async with lock:
            shared_data['gyro'] = data
        await uasyncio.sleep(0.01)

async def read_pressure(shared_data, lock):
    while True:
        data = [time.time()]
        async with lock:
            shared_data['pressure'] = data
        await uasyncio.sleep(0.1)

async def read_temperature(shared_data, lock):
    while True:
        data = [time.time()]
        async with lock:
            shared_data['temperature'] = data
        await uasyncio.sleep(0.1)



starttime_ms = utime.ticks_ms()
starttime = time.time()
timestamp = 0
schedule_counter = 0

async def get_data(shared_data, lock):
    while True:
        async with lock:
            imu_accel = shared_data['accel']
            imu_gyro = shared_data['gyro']
            pressure_pressure = shared_data['pressure']
            imu_temperature = shared_data['temperature']

        # Calculate timestamp
        timestamp = [utime.ticks_diff(utime.ticks_ms(), starttime_ms)]
        realtime = [time.time() - starttime]

        # Write data to CSV file
        output = realtime + timestamp + pressure_pressure + imu_temperature + imu_accel + imu_gyro
        print(output)
        csv.csv_write(output)
        await uasyncio.sleep(0.01)

    
    csv.close()


async def button_test_close_csv():
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    while True:
        if button.value() == 0:
            print("button pressed")
            csv.close()
        else:
            print("button not pressed")
        await uasyncio.sleep(0.1)

async def main():
    # Create the shared data dictionary and lock
    shared_data = {'accel': [], 'gyro': [], 'pressure': [], 'temperature': []}
    lock = uasyncio.Lock()

    # Run the coroutines
    await uasyncio.gather(
        read_accel(shared_data, lock),
        read_gyro(shared_data, lock),
        read_pressure(shared_data, lock),
        read_temperature(shared_data, lock),
        get_data(shared_data, lock),
        button_test_close_csv()
    )

uasyncio.run(main())


if __name__ == "__main__":
    uasyncio.run(main())
    