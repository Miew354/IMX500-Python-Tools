import socket
import json

category = "evil_cat"  # category to trigger on
confidence = 0.8  # confidence threshold

host = "127.0.0.1" # server IP
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

        while True:
            data, addr = sock.recvfrom(1024)
            if not data:
                break
            try:
                parsed_data = json.loads(data.decode())
                detection = parsed_data.get("detection")
                if detection:
                    detection_confidence = detection["confidence"] * 100
                    if detection["category"] == category and detection_confidence >= confidence * 100:
                        print(green(f"parameters met: category={detection['category']}, confidence={detection_confidence:.2f}%"))
                    else:
                        print(red(f"parameters not met: category={detection['category']}, confidence={detection_confidence:.2f}%"))
                else:
                    print(red(f"Unexpected message: {parsed_data}"))
            except json.JSONDecodeError as ex:
                print(f"Failed to parse JSON: {ex}")
            except Exception as ex:
                print(f"Unexpected error: {ex}")

if __name__ == "__main__":
    main()