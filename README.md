# Py Automatization Devices

## Description
This repository contains Python-based automation tools designed to manage and control devices errors. The code is structured to handle different types of devices, used easy-to-use scripts for automation.

## Installation

To use this repository, clone it to your local machine and then:

Run script using Docker
```bash
docker-compose up --build
```

Run script unusing Docker
```bash
poetry install
poetry run python logging/do_it_yourself.py
```

For run tests need to use:
```bash
poetry install
poetry run pytest
```

## Multiprocessing
Also I tried implement multiprocessing, for working with big files
Context main.py:
```bash
import multiprocessing

manager = multiprocessing.Manager()
devices = manager.dict()
broken_devices = manager.list()

with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    pool.starmap(process_line, [(line, broken_devices, devices) for line in parse_log_file()])
```

Additional function
```bash
def process_line(line: str, broken_devices: list, devices: dict) -> None:
    check_device_state(line, broken_devices)
    line_split = line.split(";")
    device_counter(line_split, devices)
```
