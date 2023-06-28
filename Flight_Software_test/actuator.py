#responsible for controlling the actuators which release the payload and the parachute
from machine import Pin
import time
import uasyncio # Using async from MicroPython
import comms
import sensor_data
import neopixel

# init Motor pwm
motor = machine.PWM(Pin(14, Pin.OUT), freq=50, duty=0)

async def release_CanSat():
    print("\nReleasing CanSat")
    motor.duty(100)
    await uasyncio.sleep_ms(100)
    motor.duty(0)


# sdcard_status
# accel_status
# gyro_status
# pressure_status
# temperature_status
# write_data_status
# esp32_status
# esp32_command
# receiver_status

total_status = False

np = neopixel.NeoPixel(Pin(12), 1)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255, 165, 0)
violett = (238, 130, 238)


async def update_LED():
    while True:
        if comms.esp32_command and comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status: # indicates fully operational
            np[0] = green
            np.write()
        elif not comms.esp32_command and not comms.esp32_status and not comms.receiver_status and sensor_data.sdcard_status and not sensor_data.accel_status and not sensor_data.gyro_status and not sensor_data.pressure_status and not sensor_data.temperature_status and not sensor_data.write_data_status: # indicates planned standby
            np[0] = blue
            np.write()
        elif comms.esp32_command and not comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            np[0] = orange # Everything is fine except the ESP32-CAM
            print("ESP32-CAM not responding")
            np.write()
        elif comms.esp32_command and comms.esp32_status and not comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            np[0] = violett # Everything is fine except the receiver
            print("Sensors not responding")
            np.write()
        else:
            np[0] = red
            np.write()

        print(
            "esp32_command: {} | esp32: {} | receiver: {} | sdcard: {} | accel: {} | gyro: {} | pressure: {} | temperature: {} | write_data: {}".format(comms.esp32_command, comms.esp32_status, comms.receiver_status, sensor_data.sdcard_status, sensor_data.accel_status, sensor_data.gyro_status, sensor_data.pressure_status, sensor_data.temperature_status, sensor_data.write_data_status)
        )

        await uasyncio.sleep(0.5)

def reset_status(): # currently not used
    comms.esp32_status = False
    comms.receiver_status = False
    sensor_data.sdcard_status = False
    sensor_data.accel_status = False
    sensor_data.gyro_status = False
    sensor_data.pressure_status = False
    sensor_data.temperature_status = False
    sensor_data.write_data_status = False