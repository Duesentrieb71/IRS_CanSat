# Das actuator Programm, das den Motor steuert und die LED aktualisiert.

# Benötigte Bibliotheken
from machine import Pin
import uasyncio # Using async from MicroPython
import comms
import sensor_data
import neopixel

# Motor H-Brücke (GP16/GP17)
motor_1 = Pin(16, Pin.OUT)
motor_2 = Pin(17, Pin.OUT)

# Funktion zum Steuern der H-Brücke
async def Motor_H_Bridge(direction):
    if direction == 1:
        motor_1.value(1)
        motor_2.value(0)
    elif direction == 2:
        motor_1.value(0)
        motor_2.value(1)
    elif direction == 0:
        motor_1.value(0)
        motor_2.value(0)




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

# Die LED und ihre Farben werden definiert
np = neopixel.NeoPixel(Pin(12), 1)
green = (0, 255, 0) # Werte beschreiben die Farbe in Rot, Grün, Blau Anteilen
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255, 165, 0)
violett = (238, 130, 238)

# Funktion zum Aktualisieren der LED. Es wird der Status jeder Komponente überprüft und die LED entsprechend eingestellt.
async def update_LED():
    while True:
        if comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status: # voll funktionsfähig
            np[0] = green
            np.write()
        elif not comms.esp32_status and not comms.receiver_status and sensor_data.sdcard_status and not sensor_data.accel_status and not sensor_data.gyro_status and not sensor_data.pressure_status and not sensor_data.temperature_status and not sensor_data.write_data_status: # geplanter Standby
            np[0] = blue
            np.write()
        elif not comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            np[0] = orange # voll funktionsfähig außer ESP32-CAM
            np.write()
        elif comms.esp32_status and not comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            np[0] = violett # voll funktionsfähig außer Empfänger
            np.write()
        else:
            np[0] = red
            np.write()

        # print("esp32: {} | receiver: {} | sdcard: {} | accel: {} | gyro: {} | pressure: {} | temperature: {} | write_data: {}".format(comms.esp32_status, comms.receiver_status, sensor_data.sdcard_status, sensor_data.accel_status, sensor_data.gyro_status, sensor_data.pressure_status, sensor_data.temperature_status, sensor_data.write_data_status))

        await uasyncio.sleep(0.5)

def reset_status():
    comms.esp32_status = False
    comms.receiver_status = False
    sensor_data.sdcard_status = False
    sensor_data.accel_status = False
    sensor_data.gyro_status = False
    sensor_data.pressure_status = False
    sensor_data.temperature_status = False
    sensor_data.write_data_status = False