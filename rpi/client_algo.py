import socket
import json
from environment import Environment, Obstacle


HEADER = 64 #fixed length 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Change to your laptop host ip when connected to RPI Wifi
# use ipconfig to find your laptop host ip 
HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
# HOST = '192.168.80.27'  #Cy Laptop (RPICy)

PORT = 2040 #5050 got trojan 
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(obj):
    message = obj.to_dict() if hasattr(obj, 'to_dict') else obj
    serialized_obj = json.dumps(message)
    obj_length = len(serialized_obj)
    send_length = str(obj_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    print("Sending to Server:",serialized_obj,"\n")
    client.send(serialized_obj.encode(FORMAT))
    
    # Wait for and print the main JSON response from the server
    response_header = client.recv(HEADER).decode(FORMAT).strip()
    if response_header:
        response_length = int(response_header)
        main_response = client.recv(response_length).decode(FORMAT)
        print("Response from server:", main_response, "\n")
        return main_response

    return None




# params (size_x, size_y, robot_x, robot_y, robot_direction)
env = Environment(100, 100, 10, 10, 'N')  # Create environment
env.add_obstacle(Obstacle(20, 20, 1, 5))  # Add an obstacle

response_received = None
try_count = 1

while not response_received:
    if try_count > 1:
        env.to_retry()
    response_received = send(env)
    try_count += 1

print("Extracting the data from response\n")
# send(DISCONNECT_MESSAGE)
