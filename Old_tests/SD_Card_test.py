from machine import I2C, Pin, SPI
from lib.imu import MPU6050
from lib.bmp280 import BMP280
from lib.csv import CSV
from lib import sdcard
import uos
import utime
import time

#sdcard.mount()

# Es wird geprüft, welche Ordner existieren und für das erstellen des nächsten Ordners wird inkrementiert
folder_number = 1


# Der Ordner wird erstellt
try:
    uos.mkdir('/sd/{}'.format(folder_number))
except:
    pass


header = ['time', 'pressure', 'temperature', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']

starttime_ms = utime.ticks_ms()

timestamp = 0

csv = CSV('/data3.csv'.format(folder_number), header)
while timestamp < 100000:
    long_string = [timestamp, "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd", "sdsdsdsdsdsdsd"]
    csv.csv_write(long_string)
    timestamp = utime.ticks_diff(utime.ticks_ms(), starttime_ms)
    print(timestamp)
csv.close()
