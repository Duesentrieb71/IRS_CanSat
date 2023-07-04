import time
import uasyncio # Using async from MicroPython
from lib.ibus import IBus
import actuator
from machine import Pin
import os
os.dupterm(None)  # Detach UART 0 from the REPL

# Erstellen eines IBus-Objekts (IBus ist ein Protokoll zur Kommunikation zwischen Empfänger und Mikrocontroller)
ibus_in = IBus(0, 115200, 10)

# Frequenz der Signalabfrage
get_status_Hz = 2

# Empfänger Status
receiver_status = False

# Funktion zum Empfangen des Signals vom Empfänger
async def get_receiver_status():
    global receiver_status
    while True:
        res = ibus_in.read() # einlesen des Signals vom Empfänger
        # wenn ein Signal empfangen wurde, wird der Wert des 8. Kanals ausgegeben
        if (res[0] == 1):
            # Status des Empfängers und den Wert des 8. Kanals aus
            status_ch8 = IBus.normalize(res[8])
            print ("Status {} Ch 8 {}".format(1, status_ch8), end="")
            print(" - {}".format(time.ticks_ms()))
            # Wenn der Wert des 8. Kanals größer als 50 ist und der Motor aus ist, wird der Motor eingeschaltet
            if (status_ch8 > 50 and actuator.motor_status == False):
                await actuator.start_Motor()
            elif (status_ch8 < 50 and actuator.motor_status == True):
                await actuator.stop_Motor()
            receiver_status = True
        else:
            print ("Status offline {}".format(res[0]))
            receiver_status = False
        
        await uasyncio.sleep(1/get_status_Hz)

# Kommando an den ESP32
esp32_command = False
# Status des ESP32
esp32_status = False

to_esp32 = Pin(8, Pin.OUT)
to_esp32.value(esp32_command)
from_esp32 = Pin(9, Pin.IN)

def switch_esp32_command():
    global esp32_command
    # switch to_esp32 to the opposite state
    esp32_command = not esp32_command
    to_esp32.value(esp32_command)

async def check_esp32_status():
    global esp32_status
    # check if from_esp32 is high
    while True:
        if from_esp32.value():
            esp32_status = True
            await uasyncio.sleep(1) # slower Pin reading rate when esp32 is operational (for performance)
        else:
            esp32_status = False
            await uasyncio.sleep(0.2)

if __name__ == "__main__":
    uasyncio.run(get_receiver_status())
