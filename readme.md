# IMX500 Python Tools

This repository contains Python tools for working with the Raspi IMX500 sensor. The tools provided here will help you interface with the sensor and process data.

## Installation (Raspi Only)

To install the required dependencies, run:

```bash
sudo chmod +x install.sh
./install.sh
```
Activate the environment:

```bash
source IMX500-Python-Tools/bin/activate
```
## Tools

### model_chacher/model_cacher.py

    A simple script that caches a selected model on the IMX500 by starting and stopping the camera. 

### socket_detections_stream/app.py

This script pipes the detections to a Unix socket in JSON format.

#### Usage

To start the server then pipe and echo generated mock detections:

```bash
python ./app.py start mock --verbose
```

To start the server, camera then pipe and echo IMX500 detections:

```bash
python ./app.py start camera --verbose
```

To stop the server:

```bash
python ./app.py stop
```

#### Test Clients:

There's two example client scripts that connect to the socket and process streamed detection data.

