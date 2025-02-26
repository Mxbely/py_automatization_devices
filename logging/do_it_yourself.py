# import multiprocessing
from typing import Generator

FILE_PATH = "logging/app_2.log"

ERRORS = {
    0: "Battery device error",
    1: "Temperature device error",
    2: "Threshold central error",
}


def parse_log_file() -> Generator[str, None, None]:
    return (
        row.replace("'", "").split()[-1]
        for row in open(FILE_PATH)
        if "BIG" in row
    )


def check_device_state(line: str, broken_devices: list) -> None:
    if "DD" in line:
        broken_devices.append(line)


def print_errors(id: str, errors: list) -> None:
    if "1" in errors:
        for index, number in enumerate(errors):
            if number == "1":
                print(f"{id}: {ERRORS[index]}")
    else:
        print(f"{id}: Unknown divice error")


def detailed_info_by_broken_diveces(broken_devices: list) -> None:
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
    if line[2] not in devices:
        devices[line[2]] = (
            {"state": line[-2], "count": 0}
            if line[-2] == "DD"
            else {"state": line[-2], "count": 1}
        )
    else:
        if devices[line[2]]["state"] != "DD":
            if line[-2] != "DD":
                devices[line[2]]["count"] += 1
            else:
                devices[line[2]]["state"] = line[-2]
        else:
            if line[-2] != "DD":
                devices[line[2]]["count"] += 1


# ========For multiprocessing========
def process_line(line: str, broken_devices: list, devices: dict) -> None:
    check_device_state(line, broken_devices)
    line_split = line.split(";")
    device_counter(line_split, devices)


def main() -> None:
    # ========For multiprocessing========
    # For some reason this isn't working.
    # But i tried to implement it.

    # manager = multiprocessing.Manager()
    # devices = manager.dict()
    # broken_devices = manager.list()

    # with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    #     pool.starmap(process_line, [(line, broken_devices, devices) for line in parse_log_file()])
    # ===================================
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

    detailed_info_by_broken_diveces(broken_devices)


if __name__ == "__main__":
    main()
