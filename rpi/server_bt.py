from bluetooth import *
import socket
import os
import time

class BluetoothServer:
    def __init__(self):
        # make RPi discoverable
        os.system("sudo hciconfig hci0 piscan")
        os.system("sudo chmod o+rw /var/run/sdp")

        RFCOMM_CHANNEL = 1
        #self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock = BluetoothSocket(RFCOMM)
        #self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.server_sock.bind(("", RFCOMM_CHANNEL))
        
        self.server_sock.bind(("", PORT_ANY))
        #self.server_sock.bind(("", 1))

        self.server_sock.listen(5)
        self.port = self.server_sock.getsockname()[1]
        # self.server_sock.bind(("192.168.16.16",1))
        
        if self.port != 1:
            print("close and reconnect")
            
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
        advertise_service(self.server_sock, "MDP-Server Group 16",
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE])
        
        
        print("Waiting for connection on RFCOMM channel %d" % self.port)
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)
        print("[CONNECTED] to Android Bluetooth.")

    def receive_data(self):
        try:
            data = self.client_sock.recv(1024)
            data = data.decode('utf-8')
            # print("Received %s" % data)
            # self.client_sock.send(data.encode('utf-8'))
            return data
            
        except IOError:
            pass

    def send_data(self, data):
        try:
            self.client_sock.send(data.encode('utf-8'))
        except Exception as e:
            print(e)

    def close_connection(self):
        print("[DISCONNECTED] from Android Bluetooth.")
        self.client_sock.close()
        self.server_sock.close()
        print("All done")

if __name__ == "__main__":
    #print("['']")
    bt_server = BluetoothServer()
    first_time = True

    try:
        data = bt_server.receive_data()
        print(f"data = {data}")

        while True:
            if first_time:
                robot_messages = [
                    "ROBOT/1/2/N",
                    "ROBOT/10/3/N",
                    "ROBOT/5/4//E"  # Assuming you want to include a sleep after this message as well
                ]

                for message in robot_messages:
                    bt_server.send_data(message)
                    time.sleep(1)  # Sleep for 1 second after each message

                count = 1
                for i in range(11, 13):  # Note that the end value in range is exclusive, so use 41 to include 40
                    message = f"TARGET/{count}/{i}"
                    bt_server.send_data(message)
                    count += 1
                    time.sleep(1)
                
                first_time = False

    except KeyboardInterrupt:
        bt_server.close_connection()
