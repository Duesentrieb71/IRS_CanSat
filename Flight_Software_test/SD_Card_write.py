from machine import I2C, Pin, SPI
from lib.imu import MPU6050
from lib.bmp280 import BMP280
from lib.csv import CSV
from lib import sdcard1
import uos
import utime
import time

# Assign chip select (CS) pin (and start it high)
cs = Pin(5, Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=SPI.MSB,
                  sck=Pin(2),
                  mosi=Pin(3),
                  miso=Pin(4))

# Initialize SD card
sd = sdcard1.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

header = ['time', 'pressure', 'temperature', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']

starttime_ms = utime.ticks_ms()

timestamp = 0

csv = CSV('/sd/data.csv', header)
while timestamp < 100000:
    long_string = ["sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd"]
    csv.csv_write(long_string)
    timestamp = utime.ticks_diff(utime.ticks_ms(), starttime_ms)
    print(timestamp)
csv.close()
