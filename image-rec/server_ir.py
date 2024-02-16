import socket
from datetime import datetime
from predict import predict_id
from id_mapping import mapping

# Change to your laptop host ip when connected to RPI Wifi
# use ipconfig to find your laptop host ip 
# HOST = '192.168.93.1' #Aaron Laptop (MDPGrp16)
#HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
HOST = '192.168.80.27'  #Cy Laptop (RPICy)

PORT = 2030 
HEADER_SIZE = 10        # Number of bytes to use for the header
BUFFER_SIZE = 4096      # Standard size for buffer

def receive_file(conn):
    try:
        # Receive the header containing the file name size
        file_name_size = conn.recv(HEADER_SIZE)
        if not file_name_size:
            return None  # Connection closed or error

        file_name_size = int(file_name_size.decode().strip())
        # Receive the file name
        file_name = conn.recv(file_name_size).decode()

        # Receive the header containing the direction size
        direction_size = conn.recv(HEADER_SIZE)
        if not direction_size:
            return None  # Connection closed or error

        direction_size = int(direction_size.decode().strip())
        # Receive the direction
        direction = conn.recv(direction_size).decode()

        
        # Receive the header containing the image size
        img_size = conn.recv(HEADER_SIZE)
        if not img_size:
            return None  # Connection closed or error
        
        img_size = int(img_size.decode().strip())
        data = bytearray()

        # Receive the file data
        while len(data) < img_size:
            packet = conn.recv(min(BUFFER_SIZE, img_size - len(data)))
            if not packet:
                break
            data.extend(packet)

        file_path = f"images/{file_name}"

        # Save the file data to a file with the received name
        with open(file_path, 'wb') as file:
            file.write(data)
        return file_path, direction

    except Exception as e:
        print(f"Error receiving file: {e}")
        return None, None  # Return None values indicating an error occurred

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")


        while True:  # Keep server running to accept multiple connections
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                file_path, direction = receive_file(conn)
                if file_path and direction:
                    print("File received and saved successfully.")
                    print(f"Direction received: {direction}")
                    class_name = predict_id(file_path)  # Perform prediction
                    class_id = str(mapping[class_name])
                    print(f"Predicted ID: {class_id}")
                    # Send back prediction ID to client
                    conn.sendall(class_id.encode('utf-8'))
                else:
                    print("Failed to receive file.")

start_server()
