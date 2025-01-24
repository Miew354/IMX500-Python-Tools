#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update package list and install system dependencies
sudo apt update
sudo apt install python3-pip libopencv-dev python3-picamera2 -y 

# Install IMX500 firmware
sudo apt install imx500-all -y

# Install/Upgrade pip and related modules
pip install --upgrade pip
pip install opencv-python
pip install -r requirements.txt

echo "Setup complete. You can now run the applications"

# Reboot option:
read -p "Reboot recommended. Reboot now? (y/n): " choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    sudo reboot
fi