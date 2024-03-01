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

#irFlag=0

def ir_server(stm32_queue, ir_queue, R_queue):

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

    while running_flag[0]:
        #print("inside IR while loop")
        if not R_queue.empty():
            print("Inside if branch...")
            #ir_start_event.wait()
            #ir_start_event.clear()

            #result = ir_queue.get()
            # print(f"substring is {substring}")
            # print(f"Taking a photo for obstacle no {number_part}")
            # print(f"Direction is {direction}")
            file_path = take_pic()
            #print()
            predict_id = client.send_file(file_path, "C")
            time.sleep(1.0)
            result = ir_queue.put(predict_id)
            # bt_queue.put(("IR", number_part, predict_id, direction))
            # bt_start_event.set()

    print("Disconnecting from Image Rec Server")
    client.disconnect()

def startSTMServer(stm32_queue, running_flag, ir_queue):
    print("Connecting to STM...")
    STM = STM32Server()
    STM.connect()

    while running_flag[0]:
        if not stm32_queue.empty():
            stm_start_event.wait()
            stm_start_event.clear()

            msg, associated_path = stm32_queue.get()
            print(f"stm32 queue msg = {msg}")
            STM.send(msg)
            received_msg = None
            while True:
                received_msg = STM.recv()
                if received_msg:
                    print(f"Received from stm: {received_msg}")
                    break
                # print(f"Received from stm: {received_msg}")
                # if received_msg == "R":
                #     print(f"Received R from stm: {received_msg}")
                #     break
                    
            # if associated_path:
            #     bt_queue.put(("STM32", msg, associated_path))
            #     bt_start_event.set()
            # else:
            #     algo_start_event.set()         
        
    print("Disconnecting from STM")
    STM.disconnect()


def a5_main(stm32_queue, ir_queue, R_queue):
    # HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
    # #HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
    # # HOST = '192.168.80.27'  #Cy Laptop (RPICy)
    # PORT = 2030
    irFlag=0
    STM = STM32Server()
    STM.connect()

    roundCount = 1
    STM.send("FW030")
    time.sleep(0.5)
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
                #file_path = take_pic()
                #predict_id = ImageRecognitionClient(HOST, PORT).send_file(file_path, "C")
                # result= predict_id
                R_queue.put('A')
                time.sleep(2.0)
                result = ir_queue.get()

                if (result == "41" or "-1"):
                    roundCount+=1
                    STM.send("FR090")
                    break
                elif(result!="41" or result !="-1"):
                    print(f"Predict image is{result} ")
                    irFlag=-1
                    STM.disconnect()
                    print("[DISCONNECTING] STM is disconnecting...")

            else:
                continue


#a5_main(stm32_queue, ir_queue)

if __name__ == "__main__" or "__init__":
    # # Queues for communication between threads
    # bt_queue = queue.Queue()
    ir_queue = queue.Queue()
    stm32_queue = queue.Queue()
    R_queue = queue.Queue()
        

    # At the beginning of your main section
    # bt_start_event = threading.Event() 
    # algo_start_event = threading.Event()  
    ir_start_event = threading.Event() 
    stm_start_event = threading.Event() 

    # Flag to control the execution of threads
    running_flag = [True]

    # Creating threads for each task
    threads = [
        threading.Thread(target=startSTMServer, args=(stm32_queue, running_flag, ir_queue)),
        threading.Thread(target=ir_server, args=(stm32_queue, ir_queue, R_queue)),
        #threading.Thread(target=startSTMServer, args=(stm32_queue, bt_queue, running_flag)),
        threading.Thread(target=a5_main, args=(stm32_queue, ir_queue, R_queue)),
    ]

    # Starting threads
    for thread in threads:
        thread.start()

    # Waiting for all threads to complete before exiting the main thread
    for thread in threads:
        thread.join()

    print("Task completed.")

