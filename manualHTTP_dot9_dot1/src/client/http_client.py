# src/client/http_client.py
import socket

HOST = '127.0.0.1'
PORT = 8080

def send_request(path):
    """
    Connect to the server, send a raw GET request, and print the response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Construct HTTP/0.9-style GET request as bytes
        request_line = f"GET /{path}\r\n"
        print(f"[INFO] Sending request: {request_line.strip()}")
        s.sendall(request_line.encode('utf-8'))

        # Receive response (raw bytes)
        response = b''
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk

        # Decode and print
        print("[RAW RESPONSE BYTES]", response)
        print("[DECODED RESPONSE]")
        print(response.decode('utf-8'))

if __name__ == "__main__":
    # Example: request "hello.txt" from server
    send_request("hello.txt")
