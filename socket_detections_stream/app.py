"""
Pipe the detections to the Unix socket in JSON format.

Args:
    start: start the server
    stop: stop the server
    mock: generate and pipe mock detections
    camera: pipe camera detections
    --verbose: print detection messages

Usage:
    python detections_queue.py [start|stop] [mock|camera]

TODO:
    - Allow parsing of bounding box coordinates and camera resolution
    - Add arguments for camera resolution
"""

import sys
import queue
import socket
import threading
import os
import random
import time
import json
from config import stream_freq, detection_timeout, queue_maxsize, labels_path, use_udp, udp_host, udp_port
from camera import manage_camera, get_detections

class DetectionQueue(queue.Queue):
    """Queue to store AI detections."""
    def __init__(self, maxsize=0, verbose=False):
        super().__init__(maxsize=maxsize)
        self.lock = threading.Lock()
        self.verbose = verbose

    def add_detection(self, detection):
        with self.lock:
            if self.full():
                removed_detection = self.get()  # Remove the oldest detection if full
                if self.verbose:
                    print("Queue is full. Removed oldest detections:", removed_detection)
            self.put((detection, time.time()))
            if self.verbose:
                print(f"Detection added: {detection}")

    def get_detection(self):
        with self.lock:
            while not self.empty():
                return self.get()[0] 
            return None

    def detection_timeout_func(self):
        """Remove detections that have been in the queue longer than detection_timeout."""
        while True:
            with self.lock:
                current_time = time.time()
                if detection_timeout <= 0:
                    return
                while not self.empty():
                    detection, timestamp = self.queue[0]
                    if current_time - timestamp > detection_timeout:
                        removed_detection = self.get()
                        if self.verbose:
                            print("Detection Timeout:", removed_detection)
                    else:
                        break
            time.sleep(detection_timeout)

server_socket = None
client_id_counter = 0

def unix_socket_server(socket_path, detection_queue: DetectionQueue):
    """Unix socket server that sends queued detections to connected clients."""
    global server_socket 
    clients = {}

    if os.path.exists(socket_path):
        os.remove(socket_path)

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(socket_path)
    server_socket.listen()

    def handle_client(client_sock):
        global client_id_counter
        client_id = client_id_counter
        client_id_counter += 1
        clients[client_sock] = client_id
        print(f"Client {client_id} connected")
        try:
            while True:
                detection = detection_queue.get_detection()
                if detection is not None:
                    message = (json.dumps(detection) + "\n").encode()
                    for client in list(clients.keys()):
                        try:
                            client.sendall(message)
                        except:
                            print(f"Client {clients[client]} disconnected")
                            clients.pop(client, None)
                    
        finally:
            clients.pop(client_sock, None)
            client_sock.close()

    print(f"Server started. Listening on {socket_path}")
    while True:
        try:
            client_conn, _ = server_socket.accept()
            print("Client connecting...")
            client_thread = threading.Thread(target=handle_client, args=(client_conn,))
            client_thread.daemon = True
            client_thread.start()
        except OSError:
            # Server closed
            print("Server stopped.")
            break

def udp_server(host, port, detection_queue: DetectionQueue):
    """UDP socket for debug. Mimics functionality of the Unix socket."""
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.settimeout(0.1)
    
    clients = set()
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            if addr not in clients:
                clients.add(addr)
                print(f"New UDP client: {addr}")
        except socket.timeout:
            pass
        if not clients:
            continue
        detection = detection_queue.get_detection()
        if detection:
            message = (json.dumps(detection) + "\n").encode()
            for client_addr in list(clients):
                server_socket.sendto(message, client_addr)
                try:
                    server_socket.recv
                except socket.timeout:
                    pass
                # Send any available detection to all known clients
                detection = detection_queue.get_detection()
                if detection:
                    message = (json.dumps(detection) + "\n").encode()
                    for client_addr in list(clients):
                        try:
                            server_socket.sendto(message, client_addr)
                            # Check for client heartbeat
                            server_socket.settimeout(1)
                            server_socket.recvfrom(1024)
                        except socket.timeout:
                            print(f"Client {client_addr} timed out")
                            clients.remove(client_addr)

def generate_mock_detections():
    """Generate mock detections."""
    categories = ["person", "bicycle", "car", "motorcycle", "airplane", "evil_cat"]
    detections = [
        {"category": random.choice(categories), "confidence": random.uniform(0.5, 1.0)}
        for _ in range(random.randint(1, 5))
    ]
    return detections

def mock_detections(detection_queue: DetectionQueue):
    """Generate and add mock detections to the queue."""
    while True:
        detections = generate_mock_detections()
        for detection in detections:
            detection_queue.add_detection(detection)
        time.sleep(stream_freq)

def detections_pipe(detection_queue: DetectionQueue):
    """Grab camera detections, and add them to the queue."""
    #start camera
    intrinsics = manage_camera(start=True)

    #get labels
    if intrinsics.labels is None:
        with open(labels_path, "r") as f:
            intrinsics.labels = f.read().splitlines()
    labels = intrinsics.labels

    #pipe detections
    while True:
        detections = get_detections()
        for detection in detections:

            label_conf = {
                "category": labels[int(detection.category)],
                "confidence": float(detection.conf)
            }
            
            detection_queue.add_detection(label_conf)
        time.sleep(stream_freq)

detectionQ = DetectionQueue(maxsize=queue_maxsize)

def start_server(mode, verbose=False):
    if use_udp:
        print(f"UDP mode enabled on {udp_host}:{udp_port}")
        threading.Thread(
            target=udp_server,
            args=(udp_host, udp_port, detectionQ),
            daemon=True
        ).start()
    else:
        threading.Thread(
            target=unix_socket_server,
            args=("/tmp/detections.sock", detectionQ),
            daemon=True
        ).start()
    if mode == "mock":
        threading.Thread(
            target=mock_detections,
            args=(detectionQ,),
            daemon=True
        ).start()
    elif mode == "camera":
        threading.Thread(
            target=detections_pipe,
            args=(detectionQ,),
            daemon=True
        ).start()
    if detection_timeout > 0:
        threading.Thread(
            target=detectionQ.detection_timeout_func,
            args=(detectionQ,),
            daemon=True
        ).start()

def stop_server():
    """Close the server socket if running."""
    if server_socket:
        server_socket.close()
    if mode == "camera":
        print("Stopping camera...")
        manage_camera(start=False)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python detections_queue.py [start|stop] [mock|camera] [--verbose]")
        sys.exit(1)

    command = sys.argv[1]
    mode = sys.argv[2]
    verbose = "--verbose" in sys.argv

    detectionQ = DetectionQueue(maxsize=queue_maxsize, verbose=verbose)

    if command == "start":
        start_server(mode, verbose)
        print("Press Ctrl+C to exit...")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            stop_server()
    elif command == "stop":
        stop_server()
    else:
        print("Invalid command. Use 'start' or 'stop'.")
        sys.exit(1)