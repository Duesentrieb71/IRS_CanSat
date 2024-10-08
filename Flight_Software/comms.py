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
logging_status = False

async def logging_check(break_condition = True):
    global logging_status
    while True:
        if logging_status == break_condition:
            break
        await uasyncio.sleep(0.1)


# Funktion zum Empfangen des Signals vom Empfänger
async def get_receiver_status():
    global receiver_status
    global logging_status
    while True:
        res = ibus_in.read() # einlesen des Signals vom Empfänger
        # wenn ein Signal empfangen wurde, wird der Wert des 9. Kanals ausgegeben
        if (res[0] == 1):
            status_ch9 = IBus.normalize(res[9])
            # Je nach Position des Schalters wird der Motor in die eine oder andere Richtung gedreht oder gestoppt
            if (status_ch9 == -100): # Der Schalter ist standardmäßig oben. Dabei soll der Motor ausgeschaltet sein.
                await actuator.Motor_H_Bridge(0)
            elif (status_ch9 == 0):
                await actuator.Motor_H_Bridge(1)
            elif (status_ch9 == 100):
                await actuator.Motor_H_Bridge(2)
            status_ch8 = IBus.normalize(res[8])
            if (status_ch8 == -100):
                logging_status = False
            elif (status_ch8 == 100):
                logging_status = True
            receiver_status = True
        else:
            receiver_status = False
        
        await uasyncio.sleep(1/get_status_Hz)

# Kommando an den ESP32
esp32_command = False
# Status des ESP32
esp32_status = False

to_esp32 = Pin(8, Pin.OUT)
to_esp32.value(esp32_command)
from_esp32 = Pin(9, Pin.IN, Pin.PULL_DOWN)

def esp32_on():
    global esp32_command
    to_esp32.value(1)
    esp32_command = True

def esp32_off():
    global esp32_command
    to_esp32.value(0)
    esp32_command = False

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
