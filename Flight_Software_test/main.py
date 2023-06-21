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

    # Das Programm wartet auf das Drücken des Knopfes zum Beenden der Datenaufzeichnung und des Empfangens des Funk-Signals
    await uasyncio.gather(task_button_press_end)
    task_get_status.cancel()
    task_get_data.cancel()


if __name__ == "__main__":

    uasyncio.run(main())


# TODO: Add LED blinking to indicate that the program is running
# TODO: look into interrupts for the button press