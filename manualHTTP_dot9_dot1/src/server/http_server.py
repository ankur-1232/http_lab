# src/server/http_server.py
import socket

HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Arbitrary port for testing

def handle_client(conn, addr):
    """
    Handle a single client connection.
    Receives raw bytes and sends back a simple text response.
    """
    print(f"[INFO] Connected by {addr}")

    # Receive data (raw bytes)
    data = conn.recv(1024)
    if not data:
        print("[INFO] No data received. Closing connection.")
        return

    # Decode bytes to string (assuming UTF-8)
    request_text = data.decode('utf-8')
    print(f"[RAW REQUEST BYTES] {data}")
    print(f"[DECODED REQUEST] {request_text}")

    # Parse simple GET request (HTTP/0.9 style)
    lines = request_text.splitlines()
    if len(lines) > 0 and lines[0].startswith("GET"):
        # Extract path (e.g., "GET /hello.txt")
        parts = lines[0].split()
        if len(parts) >= 2:
            filepath = parts[1].lstrip('/')
            try:
                with open(filepath, 'r') as f:
                    response_body = f.read()
            except FileNotFoundError:
                response_body = "404 Not Found"

            # Send back response as raw bytes
            conn.sendall(response_body.encode('utf-8'))

    conn.close()
    print(f"[INFO] Connection with {addr} closed.\n")

def start_server():
    """
    Start a TCP server listening for incoming connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[INFO] Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    start_server()
