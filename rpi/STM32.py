import time
import serial


class STM32Server:
    def __init__(self, serial_port= "/dev/ttyUSB0", baud_rate=115200) -> None:
        self.baud_rate = baud_rate
        self.serial_port = serial_port
        self.stm = None
    #Establish connection with STM Board
    def connect(self) -> None:
        retry = True
        while retry:
            try:
                print(f"[STM] Establishing Connection with STM on Serial Port: {self.serial_port} Baud Rate: {self.baud_rate}")
                self.stm = serial.Serial(port=self.serial_port, baudrate=self.baud_rate, timeout=None)
                if self.stm is not None:
                    print(f"[STM] Established connection on Serial Port: {self.serial_port} Baud Rate: {self.baud_rate}")
                    retry = False
            except IOError as error:
                print(f"[Error] Failed to establish STM Connection, retrying connection!")
                retry = True
    
    def disconnect(self) -> None:
        print(f"[STM] Disconnecting STM ...")
        try:
                self.stm.close()
                self.stm = None
                print(f"[STM] STM has been disconnected.")
        except Exception as error:
            print(f"[Error] Failed to disconnect STM")

    def recv(self) -> str:
            #print("Receiving ...")
            try:
                if self.stm.inWaiting() > 0:
                        #message = self.stm.read(self.stm.inWaiting()).decode("utf-8").strip()
                        raw_dat = self.stm.read(1)            
                        dat = raw_dat.strip().decode()
                        # message = self.stm.read(self.stm.inWaiting()).decode().strip()
                        # print(f"Received from stm: {message}")
                        return dat
                #return None
            except Exception as error:
                    print(f"[Error] Failed to receive from STM: {str(error)}. Retrying...")

    def send(self, message) -> None:
        print('[STM] In send to STM')
        try:  
            #while True:
            #print('[STM] in while loop')
            print(f"[STM] Message to STM: {message}")
            # self.stm.write(f"{message}\n".encode("utf-8"))
            self.stm.write(f"{message}".encode())
                #if(len(message) == 
            #self.stm.write(message)
        except Exception as error:
            print(f"[Error] Failed to send to STM: {str(error)}")


if __name__ == "__main__":
    #displacement = ["center,0,reverse,15", "left,90,forward,5","right,180,forward,5"]
    STM = STM32Server()
    STM.connect()
    STM.send("FW090")

    received_msg = None

    while(True):
        received_msg = STM.recv()
        if received_msg == "R":
            print(f"Received from stm: {received_msg}")
            break

    STM.disconnect()