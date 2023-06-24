#responsible for controlling the actuators which release the payload and the parachute
from machine import Pin
import time
import uasyncio # Using async from MicroPython
import comms
import sensor_data
import neopixel

async def release_CanSat():
    print("\nReleasing CanSat in")
    for i in range(5, 0, -1):
        print(i)
        await uasyncio.sleep(1)
    print("good luck!")


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
yellow = (255, 255, 0)
red = (255, 0, 0)


async def update_LED():
    global total_status
    while True:
        if total_status: # For performance reasons this checked first and definded further down
            np[0] = green
            np.write()
        elif comms.esp32_command and comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            total_status = True # For performance reasons this is only set to True here
            np[0] = green
            np.write()
        elif not comms.esp32_command and not comms.esp32_status and not comms.receiver_status and not sensor_data.sdcard_status and not sensor_data.accel_status and not sensor_data.gyro_status and not sensor_data.pressure_status and not sensor_data.temperature_status and not sensor_data.write_data_status: # indicates planned standby
            np[0] = yellow
            np.write()
            total_status = False
        else:
            np[0] = red
            np.write()
            total_status = False

        print(
            "esp32_command: {} | esp32_status: {} | receiver_status: {} | sdcard_status: {} | accel_status: {} | gyro_status: {} | pressure_status: {} | temperature_status: {} | write_data_status: {}".format(comms.esp32_command,
                comms.esp32_status, comms.receiver_status, sensor_data.sdcard_status, sensor_data.accel_status, sensor_data.gyro_status, sensor_data.pressure_status, sensor_data.temperature_status, sensor_data.write_data_status)
        )

        if total_status:
            await uasyncio.sleep(1) # slower LED update rate when fully operational (for performance)
        else:
            await uasyncio.sleep(0.2)

def reset_status(): # currently not used
    comms.esp32_status = False
    comms.receiver_status = False
    sensor_data.sdcard_status = False
    sensor_data.accel_status = False
    sensor_data.gyro_status = False
    sensor_data.pressure_status = False
    sensor_data.temperature_status = False
    sensor_data.write_data_status = False