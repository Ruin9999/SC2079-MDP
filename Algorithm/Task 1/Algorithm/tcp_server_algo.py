import socket
import json

# Constants
HEADER = 64
PORT = 2040
SERVER = "192.168.80.27"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def create_response():
    # Create and return the JSON response
    response = {
            "commands": ["FR00", "FW10", "SNAP1", "FR00", "BW50", "FL00", "FW60", "SNAP2", "SNAP3", "SNAP4", "FIN"],
            "distance": 46.0,
            "path": [{"d": 0, "s": -1, "x": 1, "y": 1}, {"d": 2, "s": -1, "x": 5, "y": 3}, {"d": 2, "s": -1, "x": 6, "y": 9}]
    }
    return json.dumps(response)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.\n")
    try:
        # Wait for an initial message from the client (optional, depending on your protocol)
        msg_length = conn.recv(HEADER).decode(FORMAT).strip()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] Received: {msg} \n")
            
            # Prepare and send the main JSON response
            response = create_response()
            response_bytes = response.encode(FORMAT)  # Encode the JSON string to bytes
            response_header = f"{len(response_bytes):<{HEADER}}".encode(FORMAT)  # Prepare the header
            print(f"Sending Response: {response} \n")
            conn.send(response_header + response_bytes)  # Send the header followed by the response
    except ConnectionResetError:
        print(f"[CONNECTION LOST] {addr} connection lost.\n")
    except Exception as e:
        print(f"[ERROR] {addr} encountered an error: {e}\n")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}\n")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    print("[STARTING] server is starting...\n")
    start()
