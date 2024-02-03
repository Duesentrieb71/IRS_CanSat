# Das actuator Programm, das den Motor steuert und die LED aktualisiert.

# Benötigte Bibliotheken
from machine import Pin
import uasyncio # Using async from MicroPython
import comms
import sensor_data

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

# RGB LED Pins
LED_R = Pin(18, Pin.OUT)
LED_G = Pin(19, Pin.OUT)
LED_B = Pin(20, Pin.OUT)


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

# Die Funktion zum Aktualisieren der LED
async def update_LED_color(color: tuple(int, int, int)):
    LED_R.value(color[0])
    LED_G.value(color[1])
    LED_B.value(color[2])


red = (1, 0, 0) # Werte beschreiben die Farbe in Rot, Grün, Blau Anteilen
green = (0, 1, 0)
blue = (0, 0, 1)
orange = (1, 0.65, 0)
white = (1, 1, 1)

# Es wird der Status jeder Komponente überprüft und die LED entsprechend eingestellt.
async def update_LED():
    while True:
        if comms.esp32_command and comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status: # voll funktionsfähig
            await update_LED_color(green)
        elif not comms.esp32_command and not comms.esp32_status and not comms.receiver_status and sensor_data.sdcard_status and not sensor_data.accel_status and not sensor_data.gyro_status and not sensor_data.pressure_status and not sensor_data.temperature_status and not sensor_data.write_data_status: # geplanter Standby
            await update_LED_color(blue)
        elif comms.esp32_command and comms.esp32_command and not comms.esp32_status and comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            # voll funktionsfähig außer ESP32-CAM
            await update_LED_color(orange)
        elif comms.esp32_command and comms.esp32_status and not comms.receiver_status and sensor_data.sdcard_status and sensor_data.accel_status and sensor_data.gyro_status and sensor_data.pressure_status and sensor_data.temperature_status and sensor_data.write_data_status:
            # voll funktionsfähig außer Empfänger
            await update_LED_color(white)
        else:
            await update_LED_color(red)

        # print("esp32_command: {} | esp32: {} | receiver: {} | sdcard: {} | accel: {} | gyro: {} | pressure: {} | temperature: {} | write_data: {}".format(comms.esp32_command, comms.esp32_status, comms.receiver_status, sensor_data.sdcard_status, sensor_data.accel_status, sensor_data.gyro_status, sensor_data.pressure_status, sensor_data.temperature_status, sensor_data.write_data_status))

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