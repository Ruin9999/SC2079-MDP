from bluetooth import *
import os
import time

class BluetoothServer:
    def __init__(self):
        # make RPi discoverable
        os.system("sudo hciconfig hci0 piscan")
        os.system("sudo chmod o+rw /var/run/sdp")

        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        #self.server_sock.bind(("", 1))

        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]
        #self.server_sock.bind(("192.168.41.41",1))
        
        if self.port != 1:
            print("close and reconnect")
            
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
        advertise_service(self.server_sock, "MDP-Server",
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE])
        
        
        print("Waiting for connection on RFCOMM channel %d" % self.port)
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)

    def receive_data(self):
        try:
            #while True:
                #print("In while loop...")
                ##self.client_sock.send('dssjhh')
            data = self.client_sock.recv(1024)
                #print("Received %s" % data)
            data = data.decode('utf-8')
            #if len(data) == 0:
             #   break
            print("Received %s" % data)
            self.client_sock.send(data.encode('utf-8'))
                #print("Received %s" % data.encode('utf-8'))
            
            return data
            
        except IOError:
            pass

    def send_data(self, data):
        #print('in send ' + data)
        try:
            self.client_sock.send(data.encode('utf-8'))
        except Exception as e:
            print(e)

    def close_connection(self):
        print("Disconnected")
        self.client_sock.close()
        self.server_sock.close()
        print("All done")

if __name__ == "__main__":
    #print("['']")
    bt_server = BluetoothServer()
    #bt_server.send_data('Listening...')
    try:
        #messages = ['m1', 'm2']
        #for m in messages:
        while True:
            data = bt_server.receive_data()
            # algo to rpi - 15,15
            # rpi to bluetooth - (15+5)/10, (15-5)/10
            #bt_server.send_data("ROBOT,<11>,<4>,<E>");
            bt_server.send_data("START")
            time.sleep(32)
            bt_server.send_data("FINISH|PATH")
#             bt_server.send_data("TARGET|1|11|")
#             bt_server.send_data("TARGET|2|12|")
#             bt_server.send_data("TARGET|3|14|")
#             bt_server.send_data("TARGET|4|15|")
#             bt_server.send_data("TARGET|5|16|")
#             bt_server.send_data("TARGET|6|39|")

#             time.sleep(1)
#             print("0, N")
#             bt_server.send_data("ROBOT|2|2|0");
#             time.sleep(5)
#             print("90, E, right")
#             bt_server.send_data("ROBOT|8|13|90");
#             time.sleep(1)
#             print("180, S")
#             bt_server.send_data("ROBOT|2|2|180");
#             time.sleep(5)
#             print("-90, W")
#             bt_server.send_data("ROBOT|9|7|-90");

#             bt_server.send_data("TARGET|2|29");            
#             bt_server.send_data("TARGET|3|36");            
#             bt_server.send_data("TARGET|4|37");            
#             bt_server.send_data("TARGET|5|38");                         
#             bt_server.send_data("TARGET|6|39");            
#             bt_server.send_data("TARGET|7|40");            
#             bt_server.send_data("TARGET|8|33");            

            
    except KeyboardInterrupt:
        bt_server.close_connection()
