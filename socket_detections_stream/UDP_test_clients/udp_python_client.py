import socket
import json

category = "evil_cat"  # category to trigger on
confidence = 0.8  # confidence threshold

host = "192.168.15.206" # server IP
port = 5005 # server port

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def green(text):
    return colorize(text, 32)

def red(text):
    return colorize(text, 31)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b"init", (host, port))
        buffer = ""
        while True:
            data, _ = sock.recvfrom(1024)
            if not data:
                break
            buffer += data.decode()
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                try:
                    parsed_data = json.loads(line)
                    detections = parsed_data if isinstance(parsed_data, list) else [parsed_data]
                    for detection in detections:
                        detection_confidence = detection["confidence"] * 100
                        if detection["category"] == category and detection_confidence >= confidence * 100:
                            print(green(f"parameters met: category={detection['category']}, confidence={detection_confidence:.2f}%"))
                        else:
                            print(red(f"parameters not met: category={detection['category']}, confidence={detection_confidence:.2f}%"))
                except json.JSONDecodeError as ex:
                    print(f"Failed to parse JSON: {ex}")
                except Exception as ex:
                    print(f"Unexpected error: {ex}")

if __name__ == "__main__":
    main()