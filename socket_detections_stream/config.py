#Model path:
model = '/usr/share/imx500-models/imx500_network_efficientdet_lite0_pp.rpk'

#Detections labels path:
labels_path = None #not required for default model

#Detection noise threshold
detection_threshold = 0.5

#Socket streaming frequency in seconds
stream_freq = 0.5

#Camera Frame rate
frame_rate = 5

#Detection timeout in seconds
#Note: detection timeout only checked while a client is connected
detection_timeout = 2

#Maximum items in the detection queue
queue_maxsize = 10

#Set True to enable built in UDP mode for remote testing (Leave False for Unix socket)
use_udp = False  
udp_host = "0.0.0.0"
udp_port = 5005