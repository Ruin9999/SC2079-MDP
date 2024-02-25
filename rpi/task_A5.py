import time
import serial
from STM32 import STM32Server
from takepic import take_pic
import queue
import threading
from environment import Environment, Obstacle
import os
from com_path_mapping import map_commands_to_paths
from server_bt import BluetoothServer
from client_ir import ImageRecognitionClient
from STM32 import STM32Server

#irFlag=0

def ir_server(stm32_queue, ir_queue):

    # Change to your laptop host ip when connected to RPI Wifi
    # use ipconfig to find your laptop host ip 
    HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
    #HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
    # HOST = '192.168.80.27'  #Cy Laptop (RPICy)
    PORT = 2030
    client = ImageRecognitionClient(HOST,PORT)  # Optionally pass host and port
    print("Connecting to Image Rec Server")
    client.connect()
    print("Connected...")
    while(True):
        #stm32_queue.get()
        if(stm32_queue.get!=None):
            file_path = take_pic()
            predict_id = client.send_file(file_path, "C")
            result= predict_id
            print(result)
            ir_queue.put(result)
            

# HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
#     #HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
#     # HOST = '192.168.80.27'  #Cy Laptop (RPICy)
# PORT = 2030
# client = ImageRecognitionClient(HOST,PORT)
# STM = STM32Server()
# STM.connect()
# print("[CONNECTING] Connecting to STM...")
#print("Disconnecting from Image Rec Server")
#client.disconnect()

#def startSTMServer(stm32_queue, bt_queue, running_flag, stm_start_event, bt_start_event, algo_start_event):
    # print("Connecting to STM...")
    # STM = STM32Server()
    # STM.connect()

    # while running_flag[0]:
    #     if not stm32_queue.empty():
    #         stm_start_event.wait()
    #         stm_start_event.clear()

    #         msg, associated_path = stm32_queue.get()
    #         print(f"stm32 queue msg = {msg}")
    #         STM.send(msg)
    #         received_msg = None
    #         while True:
    #             received_msg = STM.recv()
    #             if received_msg:
    #                 print(f"Received from stm: {received_msg}")
    #                 break
    #             # print(f"Received from stm: {received_msg}")
    #             # if received_msg == "R":
    #             #     print(f"Received R from stm: {received_msg}")
    #             #     break
                    
    #         if associated_path:
    #             bt_queue.put(("STM32", msg, associated_path))
    #             bt_start_event.set()
    #         else:
    #             algo_start_event.set()         
        
    # print("Disconnecting from STM")
    # STM.disconnect()

#def startBTServer(bt_queue, algo_queue, running_flag, bt_start_event, algo_start_event):
    # print("Connecting to Android Bluetooth...")
    # bt_server = BluetoothServer()
    # receive_data = None

    # try:
    #     while True:
    #         receive_data_str = bt_server.receive_data()
    #         if receive_data_str:  # Ensure receive_data_str is not None or empty
    #             print(f"Received data from Android: {receive_data_str}")

    #             try:
    #                 # Attempt to deserialize the JSON string into a dictionary
    #                 receive_data = json.loads(receive_data_str)  # Deserialize the JSON string into a dictionary
    #                 data_type = receive_data.get('type', '')

    #                 if data_type == "START/EXPLORE":
    #                     print(f"Processing START/EXPLORE command: {receive_data}")
    #                     break 
    #                 else:
    #                     # Handle other data types or commands
    #                     print(f"Received other type of command: {receive_data}")
    #                     continue

    #             except json.JSONDecodeError:
    #                 print("Received data is not valid JSON. Retrying...")
    #                 # Handle the case where the data is not valid JSON, possibly retry or log
    #         else:
    #             print("No data received, or connection lost. Retrying...")

    #     algo_queue.put(receive_data)
    #     algo_start_event.set()

    #     while running_flag[0]:
    #         if not bt_queue.empty():
    #             bt_start_event.wait()
    #             bt_start_event.clear()

    #             msg = bt_queue.get()
    #             command, *optional_parts = msg  # Correct way to unpack
    #             android_response = None

    #             if command == "BEFORE_RUNNING":
    #                 if optional_parts:
    #                     msg_to_android = optional_parts[0]
    #                     print(f"sending status to android: {msg_to_android}")
    #                     bt_server.send_data(msg_to_android)
    #                     time.sleep(0.3)

    #             elif command == "STM32":
    #                 print(f"STM32 msg: {msg}")
    #                 if optional_parts:
    #                     msg, associated_path = optional_parts
    #                     for path in associated_path:  # Assuming associated_path is the list of dictionaries
    #                         x = path["x"]
    #                         y = path["y"]
    #                         direction_map = {0: "N", 2: "E", 4: "S", 6: "W"}
    #                         d = direction_map[path["d"]]
    #                         print(f"STM32 optional parts: msg = {msg}, x = {x}, y = {y}, d = {d}")
    #                         msg_to_android = f"ROBOT/{x}/{y}/{d}"
    #                         print(f"sending robot to android: {msg_to_android}")
    #                         bt_server.send_data(msg_to_android)
    #                         time.sleep(0.3)

    #             elif command == "IR":
    #                 print(f"IR msg: {msg}")
    #                 if optional_parts:  # This checks if there are any optional parts
    #                     # optional_parts is a list, handle accordingly
    #                     number_part, predict_id, direction = optional_parts
    #                     print(f"IR optional parts: Number part = {number_part}, Predict ID = {predict_id}, Direction = {direction}")
    #                     msg_to_android = f"TARGET/{number_part}/{predict_id}"
    #                     print(f"sending target to android: {msg_to_android}")
    #                     bt_server.send_data(msg_to_android)
    #                     time.sleep(0.3)

    #             elif command == "FIN":
    #                 print(f"FIN msg: {msg}\n")
    #                 msg_to_android = f"STATUS/Stop"
    #                 print(f"sending status to android: {msg_to_android}")
    #                 bt_server.send_data(msg_to_android)
    #                 time.sleep(0.3)
    #                 break
    #             else:
    #                 # Handle other commands or continue loop
    #                 continue
    #             # start algo event at the end
    #             algo_start_event.set()

    #     # delay the disconnection
    #     time.sleep(30)
    #     running_flag[0] = False

    #     print("Disconnecting from Android Bluetooth")
    #     bt_server.close_connection()

    # except KeyboardInterrupt:
    #     bt_server.close_connection()

def a5_main(stm32_queue, ir_queue):
    # Change to your laptop host ip when connected to RPI Wifi
    # use ipconfig to find your laptop host ip 
    # HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
    # #HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
    # # HOST = '192.168.80.27'  #Cy Laptop (RPICy)
    # PORT = 2030
    # client = ImageRecognitionClient(HOST,PORT)  # Optionally pass host and port
    # print("Connecting to Image Rec Server")
    # client.connect()
    irFlag=0
    STM = STM32Server()
    STM.connect()

    roundCount = 1
    STM.send("FW080")
    time.sleep(20)
    while (irFlag>=0):
        print("Round No. " + str(roundCount))

        while(True):
            messageRec = STM.recv()
            time.sleep(0.5)

            if (messageRec != None):
                #(substring, number_part, direction) = ir_queue.get()
                #print(f"substring is {substring}")
                #print(f"Taking a photo for obstacle no {number_part}")
                print("Taking a photo for obstacle...")
                #print(f"Direction is {direction}")
                # ir_server()
                # file_path = take_pic()
                # predict_id = client.send_file(file_path, "C")
                # result= predict_id
                stm32_queue.put('A')
                result = ir_queue.get()

                if (result == "41" or "-1"):
                    roundCount+=1
                    STM.send("FR030")
                    break
                elif(result!="41" or result !="-1"):
                    print(f"Predict image is{result} ")
                    irFlag=-1
                    STM.disconnect()
                    print("[DISCONNECTING] STM is disconnecting...")

            else:
                continue


#a5_main(stm32_queue, ir_queue)

if __name__ == "__main__":
    # # Queues for communication between threads
    # bt_queue = queue.Queue()
    ir_queue = queue.Queue()
    stm32_queue = queue.Queue()
        

    # At the beginning of your main section
    # bt_start_event = threading.Event() 
    # algo_start_event = threading.Event()  
    ir_start_event = threading.Event() 
    stm_start_event = threading.Event() 

    # Flag to control the execution of threads
    running_flag = [True]

    # Creating threads for each task
    threads = [
        threading.Thread(target=ir_server, args=(stm32_queue, ir_queue)),
        #threading.Thread(target=startSTMServer, args=(stm32_queue, bt_queue, running_flag)),
        threading.Thread(target=a5_main, args=( stm32_queue, ir_queue)),

    ]

    # Starting threads
    for thread in threads:
        thread.start()

    # Waiting for all threads to complete before exiting the main thread
    for thread in threads:
        thread.join()

    print("Task completed.")
