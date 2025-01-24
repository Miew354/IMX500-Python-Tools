#This script caches the model on the IMX500 through camera start
#uses default IMX500 firmware

import argparse
import sys
from functools import lru_cache

import numpy as np

from picamera2 import MappedArray, Picamera2
from picamera2.devices import IMX500
from picamera2.devices.imx500 import (NetworkIntrinsics, postprocess_nanodet_detection)

#change this to cache custom models 
model = "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"

imx500 = IMX500(model)
intrinsics = imx500.network_intrinsics
if not intrinsics:
        intrinsics = NetworkIntrinsics()
        intrinsics.task = "object detection"
elif intrinsics.task != "object detection":
        print("The selected model is not object detection", file=sys.stderr)
        exit()

picam2 = Picamera2(imx500.camera_num)
config = picam2.create_preview_configuration(controls={"FrameRate": 30}, buffer_count=12)

imx500.show_network_fw_progress_bar()
picam2.start(config, show_preview=False)
picam2.stop()