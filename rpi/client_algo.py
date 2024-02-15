import socket
import json

class AlgorithmClient:
    def __init__(self, host, port):
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.ADDR = (host, port)
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
            print("Connected to the Algo server.")

    def send(self, obj):
        if self.client is None:
            print("Algo Client is not connected.")
            return None

        message = obj.to_dict() if hasattr(obj, 'to_dict') else obj
        serialized_obj = json.dumps(message)
        obj_length = len(serialized_obj)
        send_length = str(obj_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))

        self.client.send(send_length)
        print("Sending to Algo Server:", serialized_obj, "\n")
        self.client.send(serialized_obj.encode(self.FORMAT))
        
        # Wait for and print the main JSON response from the server
        response_header = self.client.recv(self.HEADER).decode(self.FORMAT).strip()
        if response_header:
            response_length = int(response_header)
            main_response = self.client.recv(response_length).decode(self.FORMAT)
            print("Response from Algo server:", main_response, "\n")
            return json.loads(main_response)

        return None

    def disconnect(self):
        if self.client is not None:
            # Send a disconnect message to the server if needed
            # self.send(self.DISCONNECT_MESSAGE)
            print("Disconnecting from the Algo server.")
            self.client.close()
            self.client = None
            print("Disconnected from the Algo server.")

if __name__ == "__main__":
    HOST = '192.168.80.27'
    PORT = 2040
    client = AlgorithmClient(HOST, PORT)
    client.connect()
    env = {"size_x": 100, "size_y": 100, "robot_x": 10, "robot_y": 10, "robot_direction": 'N'}  # Example object to send
    
    response_received = client.send(env)
    if response_received:
        print("Extracting the data from response\n")
        commands = response_received["commands"] 
        print("Commands:", commands)

    client.disconnect()
