#Model path:
model = '/usr/share/imx500-models/imx500_network_efficientdet_lite0_pp.rpk'

#Detections labels path:
labels_path = None #not required for default model

#Detection noise threshold
detection_threshold = 0.5

#Socket streaming frequency in seconds
stream_freq = 0.5

#Camera Frame rate
frame_rate = 20

#Detection timeout in seconds, set to zero to disable
#Note detection_timeout is redundant if clients are connected and stream_freq < detection_timeout
detection_timeout = 0
#Frequency to check for stale detections in seconds
timeout_check_freq = 0.5

#Maximum items in the detection queue
queue_maxsize = 10

#enable UDP mode with '--udp' for remote testing
udp_host = "0.0.0.0"
udp_port = 5005