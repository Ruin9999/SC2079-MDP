import socket
import os

class ImageRecognitionClient:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.HEADER_SIZE = 10
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.connect((self.HOST, self.PORT))
        print("[CONNECTED] to the Image Rec server.")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            print("[DISCONNECTED] from the Image Rec server.")
        self.socket = None

    #def send_file(self, file_path):
    def send_file(self, file_path, direction):
        if not self.socket:
            print("Not connected to the Image Rec server.")
            return
        
        try:
            file_name = os.path.basename(file_path)
            
            # Send the file name size and file name
            file_name_encoded = file_name.encode('utf-8')
            file_name_length = str(len(file_name_encoded)).encode('utf-8')
            file_name_header = file_name_length + b' ' * (self.HEADER_SIZE - len(file_name_length))
            self.socket.sendall(file_name_header)
            self.socket.sendall(file_name_encoded)

           # Send the direction size and direction
            direction_encoded = direction.encode('utf-8')
            direction_length = str(len(direction_encoded)).encode('utf-8')
            direction_header = direction_length + b' ' * (self.HEADER_SIZE - len(direction_length))
            self.socket.sendall(direction_header)
            self.socket.sendall(direction_encoded)    
            
            # Read and send the file data
            with open(file_path, 'rb') as file:
                file_data = file.read()
            data_length = str(len(file_data)).encode('utf-8')
            header = data_length + b' ' * (self.HEADER_SIZE - len(data_length))
            self.socket.sendall(header)
            self.socket.sendall(file_data)
            print("File sent to the server.")                

            response = bytearray()  # Initialize an empty bytearray to store the response
            while True:
                chunk = self.socket.recv(1024)  # Receive a chunk of data
                if not chunk:  # If chunk is empty, this means the connection is closed or there's no more data
                    break  # Exit the loop
                response += chunk  # Append the chunk to the accumulated response data
            #predict_id = response.decode('utf-8')
            predict_id = response
            print(f"Predicted ID: {predict_id}")
            self.disconnect()  # Ensure the socket is properly closed before retrying
            self.connect()  # Re-establish the connection
            return predict_id
        except Exception as e:
            print(f"Failed to send file: {e}")
