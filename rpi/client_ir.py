import socket
import os
from takepic import take_pic  # Ensure this module correctly captures and returns an image path

# Change to your laptop host ip when connected to RPI Wifi
# use ipconfig to find your laptop host ip 
HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
# HOST = '192.168.80.27'  #Cy Laptop (RPICy)

PORT = 2030             # The port used by the server
HEADER_SIZE = 10

def send_file(file_path):
    file_name = os.path.basename(file_path)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # Send the file name size and file name
        file_name_encoded = file_name.encode('utf-8')
        file_name_length = str(len(file_name_encoded)).encode('utf-8')
        file_name_header = file_name_length + b' ' * (HEADER_SIZE - len(file_name_length))
        s.sendall(file_name_header)
        s.sendall(file_name_encoded)
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Prepare and send the image data header
        data_length = str(len(file_data)).encode('utf-8')
        header = data_length + b' ' * (HEADER_SIZE - len(data_length))  # Padding to ensure header size
        s.sendall(header)
        
        # Send the file data
        s.sendall(file_data)
        print("File sent to the server.")
        
        # Optional: Wait for server acknowledgment
        response = s.recv(1024)
        print(f"Predicted ID: {response.decode('utf-8')}")

file_path = take_pic()  # Ensure this function returns the full path of the captured image
send_file(file_path)
