import sys
from functools import lru_cache

import numpy as np

from picamera2 import MappedArray, Picamera2
from picamera2.devices import IMX500
from picamera2.devices.imx500 import (NetworkIntrinsics, postprocess_nanodet_detection)

import time
from config import model

detections = []
imx500 = IMX500(model)
picam2 = Picamera2(imx500.camera_num)

class Detection:
    def __init__(self, category, conf):
        """Create a Detection object, recording category and confidence."""
        self.category = category
        self.conf = conf

def parse_detections(metadata: dict):
    """Parse the output tensor into a list of Detection objects and confidences."""
    global detections

    np_outputs = imx500.get_outputs(metadata, add_batch=True)
    input_h = imx500.get_input_size()
    if np_outputs is None:
        return detections
    scores, classes = np_outputs[1][0], np_outputs[2][0]

    detections = [
        Detection(category, score, metadata)
        for score, category in zip(scores, classes)
    ]
    return detections

def manage_camera(start=True):
    intrinsics = imx500.network_intrinsics
    if not intrinsics:
        intrinsics = NetworkIntrinsics()
        intrinsics.task = "object detection"
    elif intrinsics.task != "object detection":
        print("The selected model is not object detection", file=sys.stderr)
        exit()

    config = picam2.create_preview_configuration(controls={"FrameRate": 5}, buffer_count=12)

    if start:
        imx500.show_network_fw_progress_bar()
        picam2.start(config, show_preview=False)
    else:
        picam2.stop()

def get_detections():
    while True:
        metadata = picam2.capture_metadata()
        detections = parse_detections(metadata)
        return detections
    
