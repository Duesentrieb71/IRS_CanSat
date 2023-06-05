from machine import I2C, Pin, SPI
from lib.imu import MPU6050
from lib.bmp280 import BMP280
from lib.csv import CSV
from lib import sdcard
import uos
import utime
import time
import uasyncio

# Assign chip select (CS) pin (and start it high)
cs = Pin(5, Pin.OUT)
# Intialize SPI peripheral (start with 1 MHz)
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
# Initialize SD card
sd = sdcard.SDCard(spi, cs = Pin(5, Pin.OUT))
# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

#set up i2c bus
i2c = I2C(id = 0, scl = Pin(1), sda = Pin(0), freq = 400000)
#set up Inertial Measurement Unit
imu = MPU6050(i2c)
#set up pressure sensor
pressure = BMP280(i2c)

header = ['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temperature', 'pressure']
csv = CSV('/sd/data.csv', header)


# Frequency of data collection
get_data_Hz = 100
accel_Hz = 100
gyro_Hz = 100
pressure_Hz = 6
temperature_Hz = 4

async def read_accel(shared_data, lock):
    while True:
        data = [imu.accel.x, imu.accel.y, imu.accel.z]
        async with lock:
            shared_data['accel'] = data
        await uasyncio.sleep(1/accel_Hz)

async def read_gyro(shared_data, lock):
    while True:
        data = [imu.gyro.x, imu.gyro.y, imu.gyro.z]
        async with lock:
            shared_data['gyro'] = data
        await uasyncio.sleep(1/gyro_Hz)

async def read_temperature(shared_data, lock):
    while True:
        data = [imu.temperature]
        async with lock:
            shared_data['temperature'] = data
        await uasyncio.sleep(1/temperature_Hz)

async def read_pressure(shared_data, lock):
    while True:
        data = [pressure.pressure]
        async with lock:
            shared_data['pressure'] = data
        await uasyncio.sleep(1/pressure_Hz)

starttime_ms = utime.ticks_ms()
starttime = time.time()
timestamp = 0
schedule_counter = 0

async def get_data(shared_data, lock):
    while True:
        async with lock:
            imu_accel = shared_data['accel']
            imu_gyro = shared_data['gyro']
            imu_temperature = shared_data['temperature']
            pressure_pressure = shared_data['pressure']

        # Calculate timestamp
        timestamp = [utime.ticks_diff(utime.ticks_ms(), starttime_ms)]
        realtime = [time.time() - starttime]

        # Write data to CSV file
        output = realtime + timestamp + imu_accel + imu_gyro + imu_temperature + pressure_pressure
        print(output)
        csv.csv_write(output)
        await uasyncio.sleep(1/get_data_Hz)

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
        read_temperature(shared_data, lock),
        read_pressure(shared_data, lock),
        get_data(shared_data, lock)
    )

if __name__ == '__main__':
    uasyncio.run(main())
