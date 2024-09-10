# Das Hauptprogramm, das die anderen Programme aufruft und die Tasks erstellt. Es wird mit uasyncio gearbeitet, um die Tasks gleichzeitig auszuführen.

# Benötigte Bibliotheken
import comms
import sensor_data
import actuator
import uasyncio # Using async from MicroPython
import machine
import time

# Um mehrere Funktionen gleichzeitig auszuführen, wird mit sogenannter asynchronen Funktionen gearbeitet. Dabei wird immer nur eine Funktion für eine sehr kurze Zeit ausgeführt, bevor die nächste dran kommt. Dies geschieht so schnell, dass es für den Menschen so aussieht, als würden die Funktionen gleichzeitig ausgeführt werden.

# Funktion zur Datenaufzeichnung und zum Empfangen des Funk-Signals
async def services():
    # Das Programm wartet auf das Drücken des Knopfes zum Starten
    # task_button_press = uasyncio.create_task(sensor_data.button_press())
    task_get_status = uasyncio.create_task(comms.get_receiver_status()) # Empfangen des Funk-Signals
    task_loggin_check = uasyncio.create_task(comms.logging_check())
    await uasyncio.gather(task_loggin_check)
    # await uasyncio.gather(task_button_press)
    # time.sleep(0.5) # Warte 0.5 Sekunden, um sicherzustellen, dass der Knopf nicht mehr gedrückt ist
    comms.esp32_on() # Schaltet die Kamera ein

    # Es werden drei Tasks erstellt, die gleichzeitig ausgeführt werden. Ein Task ist eine Funktion, die asynchron ausgeführt wird.
    task_get_data = uasyncio.create_task(sensor_data.collect_data()) # Datenaufzeichnung der Sensoren
    task_check_esp32_status = uasyncio.create_task(comms.check_esp32_status()) # Überprüfen des Status des ESP32
    task_button_press = uasyncio.create_task(sensor_data.button_press()) # Knopfdruck zum Beenden

    # Das Programm wartet auf das Drücken des Knopfes zum Beenden der Datenaufzeichnung und des Empfangens des Funk-Signals
    await uasyncio.gather(task_button_press)
    # Alles wird beendet
    sensor_data.csv.close()
    task_get_status.cancel()
    task_get_data.cancel()
    task_check_esp32_status.cancel()
    comms.esp32_off()
    actuator.reset_status() # Setzt den Status der Sensoren zurück
    await uasyncio.sleep(0.5) # Warte 0.5 Sekunden, um sicherzustellen, dass der Knopf nicht mehr gedrückt ist
    # Pi Pico neustarten
    machine.reset()


async def main():
    task_services = uasyncio.create_task(services())
    task_update_LED = uasyncio.create_task(actuator.update_LED())
    await uasyncio.gather(task_services, task_update_LED)

if __name__ == "__main__":
    uasyncio.run(main())



# TODO: look into interrupts for the button press
# TODO: (maybe) implement UART communication between the ESP32 and the pico