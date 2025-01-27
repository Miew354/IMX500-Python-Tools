#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update package list and install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv libopencv-dev python3-picamera2 -y 

# Install IMX500 firmware
sudo apt install imx500-all -y

# Create a virtual environment
cd "$(dirname "$0")"
python3 -m venv IMX500-Python-Tools
source IMX500-Python-Tools/bin/activate

# Install/Upgrade pip and related modules
pip install --upgrade pip
pip install opencv-python

#ensure dependencies are present in virtual environment
python3 -m venv --system-site-packages IMX500-Python-Tools

# Activate the virtual environment
source IMX500-Python-Tools/bin/activate

# Uninstall conflicting NumPy
pip uninstall -y numpy

# Download COCO labels for default detections
curl -o socket_detections_stream/coco_labels.txt https://raw.githubusercontent.com/amikelive/coco-labels/refs/heads/master/coco-labels-paper.txt

echo "Setup complete. You can now run the application using './run.sh'."

# Reboot option:
read -p "Reboot recommended. Reboot now? (y/n): " choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    sudo reboot
fi