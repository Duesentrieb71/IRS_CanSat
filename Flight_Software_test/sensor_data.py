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

header = ['time', 'pressure', 'temperature', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']
csv = CSV('/sd/data.csv', header)

starttime_ms = utime.ticks_ms()
starttime = time.time()
timestamp = 0
schedule_counter = 0

async def get_data():
    while True:
        #read data from sensors
        imu_accel = [imu.accel.x, imu.accel.y, imu.accel.z]
        imu_gyro = [imu.gyro.x, imu.gyro.y, imu.gyro.z]
        
        if schedule_counter % 10 == 0: #only read pressure and temperature every 10th time
            imu_temperature = [imu.temperature]
            pressure_pressure = [pressure.pressure]
            schedule_counter = 0

        #calculate timestamp
        timestamp = [utime.ticks_diff(utime.ticks_ms(), starttime_ms)]
        realtime = [time.time() - starttime]

        #write data to csv file
        output = realtime + timestamp + pressure_pressure + imu_temperature + imu_accel + imu_gyro
        print(output)
        csv.csv_write(output)   
        schedule_counter += 1
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
        
