import time
import serial

class STM32Server:
    def __init__(self, serial_port="/dev/ttyUSB0", baud_rate=115200):
        self.baud_rate = baud_rate
        self.serial_port = serial_port
        self.stm = None

    def connect(self):
        while True:
            try:
                print(f"[STM] Establishing Connection with STM on Serial Port: {self.serial_port} Baud Rate: {self.baud_rate}")
                self.stm = serial.Serial(port=self.serial_port, baudrate=self.baud_rate, timeout=None)
                print(f"[STM] Established connection on Serial Port: {self.serial_port} Baud Rate: {self.baud_rate}")
                print(f"[CONNECTED] to STM.")
                break
            except serial.SerialException as e:
                print(f"[Error] Failed to establish STM Connection: {e}. Retrying...")
                time.sleep(1)

    def disconnect(self):
        if self.stm:
            try:
                self.stm.close()
                self.stm = None
                print("[DISCONNECTED] from STM.")
            except serial.SerialException as e:
                print(f"[Error] Failed to disconnect STM: {e}")

    def recv(self):
        try:
            if self.stm.inWaiting() > 0:
                raw_data = self.stm.read(1)  # Read one byte
                data = raw_data.decode().strip()
                return data
        except serial.SerialException as e:
            print(f"[Error] Failed to receive from STM: {e}. Retrying...")

    def send(self, message):
        try:
            print(f"[STM] Sending message to STM: {message}")
            self.stm.reset_output_buffer()
            self.stm.write(message.encode())
            self.stm.flush()
        except serial.SerialException as e:
            print(f"[Error] Failed to send to STM: {e}")

if __name__ == "__main__":
    STM = STM32Server()
    STM.connect()

    commands = ["FL000","BR010"]
            
    for command in commands:
        STM.send(command)
        print(f"Sent to STM: {command}")
        while True:
            received_msg = STM.recv()
            if received_msg == "R":
                print(f"Received 'R' from STM: {received_msg}")
                break

    STM.disconnect()
