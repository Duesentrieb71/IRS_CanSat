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
    print("test1")

    # Es werden drei Tasks erstellt, die gleichzeitig ausgeführt werden
    task_get_status = uasyncio.create_task(comms.get_receiver_status()) # Empfangen des Signals
    print("test2")
    task_get_data = uasyncio.create_task(sensor_data.collect_data()) # Datenaufzeichnung
    print("test3")
    task_button_press = uasyncio.create_task(sensor_data.button_press()) # Knopfdruck zum Beenden
    print("test4")

    # Das Programm wartet auf das Drücken des Knopfes zum Beenden der Datenaufzeichnung und des Empfangens des Funk-Signals
    await uasyncio.gather(task_button_press)
    print("test5")
    sensor_data.csv.close() # Schließt die csv-Datei
    print("test6")
    task_get_status.cancel()
    print("test7")
    task_get_data.cancel()
    print("test8")
    comms.switch_esp32_command() # Schaltet die Kamera aus
    print("test9")
    #actuator.reset_status() # Setzt den Status der Sensoren zurück
    time.sleep(1)
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