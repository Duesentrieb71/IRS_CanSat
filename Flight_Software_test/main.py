import comms
import sensor_data

import uasyncio # Using async from MicroPython

# Nach der CanSat_timeout Zeit wird die Datenaufzeichnung und das Empfangen des Signals beendet
CanSat_timeout = 300 # Sekunden

# Funktion zur Datenaufzeichnung und zum Empfangen des Signals
async def main():
    # Das Programm wartet auf das Drücken des Startknopfes
    task_button_press_start = uasyncio.create_task(sensor_data.button_press_start())
    await uasyncio.gather(task_button_press_start)

    task_get_status = uasyncio.create_task(comms.get_status())
    task_get_data = uasyncio.create_task(sensor_data.collect_data())

    try:
        await uasyncio.wait_for(uasyncio.gather(task_get_status, task_get_data), timeout=CanSat_timeout)
    except uasyncio.TimeoutError:
        print("Timeout! Exiting...")
        task_get_status.cancel()
        task_get_data.cancel()

    print("done")


if __name__ == "__main__":

    uasyncio.run(main())