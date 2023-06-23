#responsible for controlling the actuators which release the payload and the parachute
from machine import Pin
import time
import uasyncio # Using async from MicroPython
import comms
import sensor_data

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
# receiver_status

total_status = False

async def update_LED():
    while True:
        if total_status: # For performance reasons this checked first and definded further down
            # LED green
            pass
        elif not comms.esp32_status:
            # LED yellow
            pass
        elif not comms.receiver_status:
            # LED blue
            pass
        elif comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            total_status = True # For performance reasons this is only set to True once all the sensors are working
        else:
            # LED red
            pass

        print(
            "esp32_status: {} | receiver_status: {} | sdcard_status: {} | accel_status: {} | gyro_status: {} | pressure_status: {} | temperature_status: {} | write_data_status: {}".format(
                comms.esp32_status, comms.receiver_status, sensor_data.sdcard_status, sensor_data.accel_status, sensor_data.gyro_status, sensor_data.pressure_status, sensor_data.temperature_status, sensor_data.write_data_status)
        )

        if total_status:
            await uasyncio.sleep(1) # slower LED update rate when fully operational (for performance)
        else:
            await uasyncio.sleep(0.2)