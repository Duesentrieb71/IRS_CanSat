import time
import uasyncio # Using async from MicroPython
from lib.ibus import IBus
import actuator

# Erstellen eines IBus-Objekts (IBus ist ein Protokoll zur Kommunikation zwischen Empfänger und Mikrocontroller)
ibus_in = IBus(1, 115200, 10)

# Frequenz der Signalabfrage
get_status_Hz = 100

# Funktion zum Empfangen des Signals vom Empfänger
async def get_status():
    while True:
        res = ibus_in.read() # einlesen des Signals vom Empfänger
        # wenn ein Signal empfangen wurde, wird der Wert des 8. Kanals ausgegeben
        if (res[0] == 1):
            # druckt den Status des Empfängers und den Wert des 8. Kanals aus
            print ("Status {} Ch 8 {}".format(res[0], IBus.normalize(res[8])), end="")
            print(" - {}".format(time.ticks_ms()))
            # wenn der Wert des 8. Kanals größer als 50 ist, wird die Funktion release_CanSat() aus actuator.py aufgerufen
            # damit sich der Wert ändert, wird an der Fernsteuerung ein Schalter umgelegt
            if (IBus.normalize(res[8]) > 50):
                await actuator.release_CanSat()
                break
        else:
            print ("Status offline {}".format(res[0]))
        # get_status 
        await uasyncio.sleep(1/get_status_Hz)

if __name__ == "__main__":
    uasyncio.run(get_status())