import comms
import sensor_data
import uasyncio # Using async from MicroPython

# Funktion zur Datenaufzeichnung und zum Empfangen des Funk-Signals
async def main():
    # Das Programm wartet auf das Drücken des Knopfes zum Starten
    task_button_press_start = uasyncio.create_task(sensor_data.button_press_start())
    await uasyncio.gather(task_button_press_start)

    # Es werden drei Tasks erstellt, die gleichzeitig ausgeführt werden
    task_get_status = uasyncio.create_task(comms.get_status()) # Empfangen des Signals
    task_get_data = uasyncio.create_task(sensor_data.collect_data()) # Datenaufzeichnung
    task_button_press_end = uasyncio.create_task(sensor_data.button_press_end()) # Knopfdruck zum Beenden

    # Sobald der Knopf gedrückt wird, wird die Datenaufzeichnung und das Empfangen des Signals beendet
    done, pending = await uasyncio.wait({task_get_status, task_get_data, task_button_press_end}, return_when=uasyncio.FIRST_COMPLETED)
    
    print("Knopf gedrückt, Aufzeichnung wird beendet")
    for task in pending:
        task.cancel()


if __name__ == "__main__":

    uasyncio.run(main())