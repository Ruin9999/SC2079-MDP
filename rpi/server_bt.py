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
    bt_server = BluetoothServer()
    print("start up")
    count = 0
    data = None
    try:
        while True:
            if count > 5:
                break
            data = bt_server.receive_data()
            if data:
                print(f"data = {data}")
                count += 1
            

        msg_to_android = f"FINISH/PATH"
        bt_server.send_data(msg_to_android)

    except KeyboardInterrupt:
        bt_server.close_connection()
