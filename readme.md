# IMX500 Python Tools

This repository contains Python tools for working with the Raspi IMX500 sensor. The tools provided here will help you interface with the sensor and process data.

## Features

- Interface with the IMX500 sensor
- Data processing utilities

## Installation (Raspi Only)

To install the required dependencies, run:

   ```bash
   sudo chmod +x install.sh run.sh
   ```
    ```bash
    ./install.sh
    ```
## Tools

### socket_detections_stream/app.py

This script pipes the detections to a Unix socket in JSON format.

#### Usage

To start the server and pipe generated mock detections:
```bash
python socket_detections_stream/app.py start mock
```

To start the server, camera and pipe IMX500 detections:
```bash
python socket_detections_stream/app.py start camera
```

To stop the server:
```bash
python socket_detections_stream/app.py stop
```

#### Test Clients:

There's two example client scripts that connect to the socket and process detection data.