from machine import I2C, Pin
from lib.imu import MPU6050
from lib.bmp280 import BMP280
from lib.csv import CSV
import time

#set up i2c bus
i2c = I2C(scl=Pin(5), sda=Pin(4))

#set up Inertial Measurement Unit
imu = MPU6050(i2c)

#set up pressure sensor
pressure = BMP280(i2c)

header = ['time', 'pressure', 'temperature', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']

csv = CSV('data.csv', header)

starttime = time.time_ns()

while True:
    imu_accel = [imu.accel.x, imu.accel.y, imu.accel.z]
    imu_gyro = [imu.gyro.x, imu.gyro.y, imu.gyro.z]
    imu_temperature = [imu.temperature]
    pressure_pressure = ["none"] #[pressure.pressure]
    timestamp = [time.time_ns() - starttime]

    output = timestamp + pressure_pressure + imu_temperature + imu_accel + imu_gyro
    
    for i in output:
        csv.csv_write(i)
        



