import time
from typing import Generator

FILE_PATH = "logging/app_2.log"

ERRORS = {
    0: "Battery device error",
    1: "Temperature device error",
    2: "Threshold central error",
}


def parse_log_file() -> Generator[str, None, None]:
    """
    Parses the log file specified by FILE_PATH and yields the last word
    of each line containing the word "BIG". The single quotes in the
    line are removed before splitting.

    Yields:
        str: The last word of each relevant line in the log file.
    """
    try:
        with open(FILE_PATH, "r") as file:
            for row in file:
                if "BIG" in row:
                    yield row.replace("'", "").split()[-1]
    except FileNotFoundError:
        print(f"Error: The file at {FILE_PATH} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def check_device_state(line: str, broken_devices: list) -> None:
    """
    Checks the state of a device from a log line and appends it
    to the broken_devices list if the device is broken.
    The device is considered broken if the line contains the substring "DD".
    """

    if "DD" in line:
        broken_devices.append(line)


def print_errors(id: str, errors: list) -> None:
    """
    Prints a specific error message for a device id
    if the error list contains a 1.
    Otherwise, it prints an unknown device error message.
    """
    if "1" in errors:
        for index, number in enumerate(errors):
            if number == "1":
                print(f"{id}: {ERRORS[index]}")
    else:
        print(f"{id}: Unknown device error")


def detailed_info_by_broken_devices(broken_devices: list) -> None:
    """
    Prints detailed information about broken devices.

    For each broken device, it prints the id and a specific error message based
    on the error bits in the device's log line.
    """
    print()
    for device in broken_devices:
        error_list = []
        device = device.split(";")
        id = device[2]
        sp = device[6][:-1] + device[13]
        groups = []

        for i in range(0, len(sp), 2):
            groups.append(sp[i : i + 2])

        binary_groups = [format(int(num), "08b") for num in groups]

        for group in binary_groups:
            error_list.append(group[4])

        print_errors(id, error_list)


def device_counter(line: str, devices: dict) -> None:
    """
    Counts the number of times a device has a successful message
    and updates the state if the device becomes broken.
    """
    device_id = line[2]
    device_state = line[-2]

    if device_id not in devices:
        devices[device_id] = {
            "state": device_state,
            "count": 0 if device_state == "DD" else 1,
        }
    else:
        # If the device is not broken, increment the count
        if devices[device_id]["state"] != "DD" and device_state != "DD":
            devices[device_id]["count"] += 1
        # If the device is broken, update its state
        elif device_state == "DD":
            devices[device_id]["state"] = "DD"
        else:
            devices[device_id]["count"] += 1


def main() -> None:
    """
    Reads the log file and prints the following information:
    - The number of all big devices
    - The number of successful big devices
    - The number of failed big devices
    - The number of success messages for each big device
    - And the detailed information for each broken device
    """
    devices = {}
    broken_devices = []

    for line in parse_log_file():
        check_device_state(line, broken_devices)
        line = line.split(";")
        device_counter(line, devices)

    failed_devices = sum(
        1 if devices["state"] == "DD" else 0 for devices in devices.values()
    )
    print("All big devices: ", len(devices))
    print("Succesful big devices: ", len(devices) - failed_devices)
    print("Failed big devices: ", failed_devices)

    print("\nSuccess messages count:")
    for device in devices:
        print(device, ": ", devices[device]["count"])

    detailed_info_by_broken_devices(broken_devices)


if __name__ == "__main__":
    main()
    time.sleep(1)  # Just for correct output in docker container
