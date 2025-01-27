#put your model path here:
model = '/usr/share/imx500-models/imx500_network_efficientdet_lite0_pp.rpk'

#detections labels path:
labels_path = None #not required for default model

#detection noise threshold
detection_threshold = 0.5

#Socket streaming frequency in seconds
stream_freq = 0.5

#detection timeout in seconds
detection_timeout = 2

#maximum items in the detection queue
queue_maxsize = 100