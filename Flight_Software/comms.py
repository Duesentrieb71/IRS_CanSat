# Das comms Programm, das die Kommunikation mit dem Empfänger und dem ESP32 regelt.

# Benötigte Bibliotheken
import uasyncio # Using async from MicroPython
from lib.ibus import IBus
import actuator
from machine import Pin
import os
os.dupterm(None)  # Detach UART 0 from the REPL

# Erstellen eines IBus-Objekts (IBus ist ein Protokoll zur Kommunikation zwischen Empfänger und Mikrocontroller)
ibus_in = IBus(0, 115200, 10)

# Frequenz der Signalabfrage
get_status_Hz = 5

# Empfänger Status
receiver_status = False

# Funktion zum Empfangen des Signals vom Empfänger
async def get_receiver_status():
    global receiver_status
    while True:
        res = ibus_in.read() # einlesen des Signals vom Empfänger
        # wenn ein Signal empfangen wurde, wird der Wert des 9. Kanals ausgegeben
        if (res[0] == 1):
            status_ch9 = IBus.normalize(res[9])
            # Je nach Position des Schalters wird der Motor in die eine oder andere Richtung gedreht oder gestoppt
            if (status_ch9 == 100): # Der Schalter ist standardmäßig oben. Dabei soll der Motor ausgeschaltet sein.
                await actuator.Motor_H_Bridge(0)
            elif (status_ch9 == 0):
                await actuator.Motor_H_Bridge(1)
            elif (status_ch9 == -100):
                await actuator.Motor_H_Bridge(2)
            receiver_status = True
        else:
            receiver_status = False
        
        await uasyncio.sleep(1/get_status_Hz)

# Status des ESP32
esp32_status = False

to_esp32 = Pin(8, Pin.OUT)
from_esp32 = Pin(9, Pin.IN)

def esp32_on():
    to_esp32.value(1)

def esp32_off():
    to_esp32.value(0)

async def check_esp32_status():
    global esp32_status
    # überprüfe den Status des ESP32
    while True:
        if from_esp32.value():
            esp32_status = True
        else:
            esp32_status = False
        await uasyncio.sleep(0.2)
        
if __name__ == "__main__":
    uasyncio.run(get_receiver_status())
