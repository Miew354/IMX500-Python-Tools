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
Includes debug options to enable easier development and testing outside of raspi, such as mock detections generator and UDP mode. 

#### Usage

```bash
python socket_stream.py [start|stop] [mock|camera] [--verbose] [--udp]
```

#### Configuration

See `config.py` for various configuration options.

#### Test Clients:

Example client scripts that connect to the relevant socket and process streamed detection data.

### TODO:
- Allow parsing of bounding box coordinates and camera resolution
- Allow custom arguments for camera resolution

