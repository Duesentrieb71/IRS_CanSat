# Das sensor_data Programm, das die Sensoren ausliest und die Daten in einer csv-Datei speichert.

# Benötigte Bibliotheken
import uos
from machine import I2C, Pin
from lib.imu import MPU6050
from lib.bmp280 import BMP280
from lib.csv import CSV
import utime
import time
import uasyncio
import lib.sdcard as sdcard

# Status der Prozesse
accel_status = False
gyro_status = False
pressure_status = False
temperature_status = False
write_data_status = False
# Status der SD Karte
sdcard_status = False


# Die SD Karte wird gemountet (verbunden), damit der Microcontroller auf die SD Karte zugreifen kann
try:
    sdcard.mount()
    sdcard_status = True
except:
    sdcard_status = False
    print("SD card not mounted")

# Es wird geprüft, welche Ordner existieren und für das erstellen des nächsten Ordners wird inkrementiert
folder_number = 1
while True:
    if '{}'.format(folder_number) in uos.listdir('/sd'):
        folder_number += 1
    else:
        break

# Der Ordner wird erstellt
try:
    uos.mkdir('/sd/{}'.format(folder_number))
except:
    pass

# Der I2C Bus wird initialisiert
try:
    i2c = I2C(id = 0, scl = Pin(1), sda = Pin(0), freq = 400000)
except:
    pass

# Die MPU6050 und BMP280 Sensoren werden initialisiert
try:
    imu = MPU6050(i2c) # IMU = Inertial Measurement Unit (Beschleunigungssensor und Gyroskop)
except:
    pass

try:
    pressure = BMP280(i2c) # BMP = Barometric Pressure Sensor (Luftdrucksensor)
except:
    pass

# Die csv-Datei wird erstellt (In einer csv-Datei werden die einzelnen Werte mit Kommas/Semikolons getrennt abgespeichert)
header = ['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temperature', 'pressure']
csv = CSV('/sd/{}/data.csv'.format(folder_number), header)


# Frequenz der Datenaufzeichnung (Hz = Hertz = 1/s)
## Was wären sinnvolle Werte für die Frequenzen?
accel_Hz = ###
gyro_Hz = 100
pressure_Hz = ###
temperature_Hz = 4
write_data_Hz = max(100, accel_Hz, gyro_Hz)

# Funktion zum Auslesen der Accelerometerdaten
async def read_accel(shared_data, lock):
    global accel_status
    while True:
        try:
            data = [imu.accel.x, imu.accel.y, imu.accel.z]
            async with lock:
                shared_data['accel'] = data
            accel_status = True
        except:
            accel_status = False
        ## Wie wird die Wartezeit anhand der Frequenz berechnet?
        await uasyncio.sleep(###)

# Funktion zum Auslesen der Gyroskopdaten
async def read_gyro(shared_data, lock):
    global gyro_status
    while True:
        try: 
            ## Welche Achsen sollen ausgelesen werden?
            data = ###
            async with lock:
                shared_data['gyro'] = data
            gyro_status = True
        except:
            gyro_status = False
        await uasyncio.sleep(1/gyro_Hz)

# Funktion zum Auslesen der Temperaturdaten
async def read_temperature(shared_data, lock):
    global temperature_status
    while True:
        try:
            data = [imu.temperature]
            async with lock: 
                ## Welchen Name hat der Schlüssel in diesem Fall?
                shared_data[###] = data
            temperature_status = True
        except:
            temperature_status = False
        await uasyncio.sleep(1/temperature_Hz)

# Funktion zum Auslesen der Druckdaten
async def read_pressure(shared_data, lock):
    global pressure_status
    while True:
        try:
            data = [pressure.pressure]
            async with lock:
                shared_data['pressure'] = data
            pressure_status = True
        except:
            pressure_status = False
        await uasyncio.sleep(1/pressure_Hz)

starttime_ms = utime.ticks_ms()
timestamp = 0

# Funktion zum Sammeln und Speichern aller Daten. Es wird ein "shared_data" Dictionary erstellt. Darin hat jeder Wert einen Schlüssel. Mit dem Schlüssel kann auf den Wert zugegriffen werden.
async def write_data(shared_data, lock):
    global write_data_status
    while True:
        try:
            # "locks" werden verwendet, um sicherzustellen, dass die Daten nicht gleichzeitig geschrieben und gelesen werden
            async with lock:
                imu_accel = shared_data['accel']
                imu_gyro = shared_data['gyro']
                imu_temperature = shared_data['temperature']
                pressure_pressure = shared_data['pressure']

            # Zeitstempel wird errechnet
            timestamp = [utime.ticks_diff(utime.ticks_ms(), starttime_ms)]

            # Alle Daten werden in einer csv-Datei gespeichert
            output = timestamp + imu_accel + imu_gyro + imu_temperature + pressure_pressure
            #print(output)
            csv.csv_write(output)
            write_data_status = True
        except:
            write_data_status = False
        await uasyncio.sleep(1/write_data_Hz)
        
async def collect_data():
    while True:
        # Create the shared data dictionary and lock
        shared_data = {'accel': [], 'gyro': [], 'pressure': [], 'temperature': []}
        lock = uasyncio.Lock()

        # Run the coroutines
        await uasyncio.gather(
            read_accel(shared_data, lock),
            read_gyro(shared_data, lock),
            read_temperature(shared_data, lock),
            read_pressure(shared_data, lock),
            write_data(shared_data, lock)
        )

async def button_press():
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    while True:
        if button.value() == 0:
            # print("button pressed")
            break
        else:
            # print("button not pressed")
            pass
        await uasyncio.sleep(0.2)

if __name__ == '__main__':
    uasyncio.run(collect_data())
