import comms
import sensor_data
import actuator
import uasyncio # Using async from MicroPython
import machine
import time

# Funktion zur Datenaufzeichnung und zum Empfangen des Funk-Signals
async def services():
    # Das Programm wartet auf das Drücken des Knopfes zum Starten
    task_button_press = uasyncio.create_task(sensor_data.button_press())
    await uasyncio.gather(task_button_press)
    time.sleep(1)
    comms.switch_esp32_command() # Schaltet die Kamera ein

    # Es werden drei Tasks erstellt, die gleichzeitig ausgeführt werden
    task_get_status = uasyncio.create_task(comms.get_receiver_status()) # Empfangen des Signals
    task_get_data = uasyncio.create_task(sensor_data.collect_data()) # Datenaufzeichnung
    task_check_esp32_status = uasyncio.create_task(comms.check_esp32_status()) # Überprüfen des Status des ESP32
    task_button_press = uasyncio.create_task(sensor_data.button_press()) # Knopfdruck zum Beenden

    # Das Programm wartet auf das Drücken des Knopfes zum Beenden der Datenaufzeichnung und des Empfangens des Funk-Signals
    await uasyncio.gather(task_button_press)
    sensor_data.csv.close() # Schließt die csv-Datei
    task_get_status.cancel()
    task_get_data.cancel()
    task_check_esp32_status.cancel()
    comms.switch_esp32_command() # Schaltet die Kamera aus
    actuator.reset_status() # Setzt den Status der Sensoren zurück
    await uasyncio.sleep(1)
    # Pi Pico neustarten
    machine.reset()


async def main():
    task_services = uasyncio.create_task(services())
    task_update_LED = uasyncio.create_task(actuator.update_LED())
    await uasyncio.gather(task_services, task_update_LED)

if __name__ == "__main__":
    uasyncio.run(main())



# TODO: look into interrupts for the button press
# TODO: implement LED signaling for the status
# TODO: (maybe) implement UART communication between the ESP32 and the pico