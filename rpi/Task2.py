import time
import queue
import threading
from datetime import datetime
import json
from environment import Environment, Obstacle
import os
#from takepic import CameraManager
from takepicV0 import take_pic
from com_path_mapping import map_commands_to_paths

from server_bt import BluetoothServer
from client_algo import AlgorithmClient
from http_client_ir import ImageRecognitionClient
from STM32 import STM32Server

DISCONNECT_MESSAGE = "!DISCONNECT"

def startIRClient(ir_queue, running_flag, ir_start_event, cmd_start_event):
    # Change to your laptop host ip when connected to RPI Wifi
    # use ipconfig to find your laptop host ip 
    # HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
    HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
    #HOST = '192.168.80.27'  #Cy Laptop (RPICy)
    PORT = 2030
    client = ImageRecognitionClient(HOST,PORT)  # Optionally pass host and port
    print("Testing Connection to IR Server...")
    # Test - Check server status
    status_response = client.check_status()  # This method should make a GET request to the /status endpoint

    if status_response and status_response.get('status') == 'OK':
        print("[CONNECTED] to IR Server\n")

        # print("Initialize and Warming up Camera")

        #camera = CameraManager()
        #camera.warm_up()

        while running_flag[0]:
            if not ir_queue.empty():
                ir_start_event.wait()

                # (substring, number_part, direction) = ir_queue.get()
                # print(f"substring is {substring}")
                # print(f"Taking a photo for obstacle no {number_part}")
                # print(f"Direction is {direction}")
                # file_path = camera.take_pic()
                file_path = take_pic()
                
                predict_id = None
                startTime = datetime.now()
                response = client.send_file(file_path, "north")
                endTime = datetime.now()
                totalTime = (endTime - startTime).total_seconds()
                print(f"Time taken for Receiving Image = {totalTime} s")

                if response is not None:  # Check if response is not None
                    predict_id = response.get('predicted_id')
                if not predict_id:
                    print("predict id is None, changing to -1")
                    predict_id = "-1"
                
                cmd_queue.put("IR", predict_id)
                ir_start_event.clear()
                cmd_start_event.set()
        #camera.close()
    else:
        print("Failed to connect to the IR server or IR server returned an unexpected status.")

def stmSendThread(STM, stm32_send_queue, stm32_recv_queue, running_flag, stm_start_event, cmd_start_event):

    while running_flag[0]:
        if not stm32_send_queue.empty():
            stm_start_event.wait()
            msg = stm32_send_queue.get()
            print(f"stm32 queue msg = {msg}")
            STM.send(msg)
            stm32_recv_queue.put(msg)
            stm_start_event.clear()
            time.sleep(0.1)


def stmRecvThread(STM, stm32_recv_queue, running_flag, cmd_start_event):
    while running_flag[0]:
        if not stm32_recv_queue.empty():
            msg = stm32_recv_queue.get(timeout=5)
            start_time = time.time()
            timeout = 3
            received_msg = None

            while(True):
                received_msg = STM.recv()
                # print(f"Received from stm: {received_msg}")
                if received_msg == "R":
                    print(f"Received R from stm: {received_msg}")
                    break
                elif (time.time()-start_time>timeout):
                    print("Timeout waiting for R receive message")
                    break
                else:
                    time.sleep(0.1)
    
            cmd_start_event.set()
            # if associated_path:
            #     bt_queue.put(("STM32", msg, associated_path))
            #     bt_start_event.set()
            # else:
            #     algo_start_event.set()

def cmdGeneratorTemp(distance_1, distance_2, width_of_obstacle2, cmd_queue, ir_queue, stm32_send_queue, cmd_start_event, stm_start_event, ir_start_event):

    # First stage: go forward and recognize first obstacle 
    command = "US020"
    stm32_send_queue.put(command)
    cmd_start_event.clear()
    stm_start_event.set()
    cmd_start_event.wait()
    ir_queue.put("SNAP")
    cmd_start_event.clear()
    ir_start_event.set()
    direction = ""
    cmd_start_event.wait()
    while True:
        if not cmd_queue.empty():
            predict_id = cmd_queue.get()
            direction = "right"
            if predict_id == 39:
                direction = "left"
            break
        else:
            print("Error: faild to get direction")
            time.sleep(1)
    print("First obstacle's arrow: ", direction)
    
    # Second stage: turn and go to second obstacle
    commands_list = []
    if direction == "right":
        commands_list = ["FR090", "FL090", "FW010", "FL090", "FR090"]
    else:
        commands_list = ["FL090", "FR090", "FW010", "FR090", "FL090"]
    
    for command in commands_list:
        cmd_start_event.wait()
        cmd_start_event.clear()
        stm32_send_queue.put((command))
        stm_start_event.set()

    command = "US020"
    stm32_send_queue.put(command)
    cmd_start_event.clear()
    stm_start_event.set()

    cmd_start_event.wait()
    ir_start_event.set()
    direction = ""
    while True:
        if not cmd_queue.empty():
            predict_id = cmd_queue.get()
            direction = "right"
            if predict_id == 39:
                direction = "left"
            break
        else:
            print("Error: faild to get direction")
    
    # Third stage: turn and go forward to another side 
    
    print("Second obstacle's arrow: ", direction)
    if direction == "right":
        commands_list = ["FR090", f"FW0{width_of_obstacle2 / 2 - 5}", "FL090", "FW010", "FL090"]
    else:
        commands_list = ["FR090", f"FW0{width_of_obstacle2 / 2 - 5}", "FL090", "FW010", "FL090"]

    if width_of_obstacle2 + 20 < 100:
        commands_list.append(f"FW0{width_of_obstacle2 + 20}")
    else:
        commands_list.append(f"FW{width_of_obstacle2 + 20}")

    if direction == "right":
        commands_list.append("FL090")
    else:
        commands_list.append("FR090")

    for command in commands_list:
        cmd_start_event.wait()
        cmd_start_event.clear()
        stm32_send_queue.put((command))
        stm_start_event.set()

    # Last stage: Go back to the carpark
        
    

if __name__ == "__main__":
    # Queues for communication between threads
    bt_queue = queue.Queue()
    algo_queue = queue.Queue()
    ir_queue = queue.Queue()
    stm32_send_queue = queue.Queue()
    stm32_recv_queue = queue.Queue()
    cmd_queue = queue.Queue()

    # At the beginning of your main section
    bt_start_event = threading.Event() 
    algo_start_event = threading.Event()  
    ir_start_event = threading.Event() 
    stm_start_event = threading.Event() 
    cmd_start_event = threading.Event()

    # Flag to control the execution of threads
    running_flag = [True]

    # init STM32 Server
    print("Connecting to STM...")
    STM = STM32Server()
    STM.connect()

    # Creating threads for each task
    threads = [
        threading.Thread(target=cmdGeneratorTemp, args={STM, 60, cmd_queue, ir_queue, stm32_send_queue, cmd_start_event, stm_start_event, ir_start_event}),
        # threading.Thread(target=startBTServer, args=(bt_queue, algo_queue, running_flag, bt_start_event, algo_start_event)),
        # threading.Thread(target=startAlgoClient, args=(algo_queue, ir_queue, stm32_send_queue, algo_start_event, bt_start_event, ir_start_event, stm_start_event)),
        threading.Thread(target=startIRClient, args=(ir_queue, running_flag, ir_start_event, cmd_start_event)),
        threading.Thread(target=stmSendThread, args=(STM, stm32_send_queue, stm32_recv_queue, running_flag, stm_start_event, cmd_start_event)),
        threading.Thread(target=stmRecvThread, args=(STM, stm32_recv_queue, running_flag, cmd_start_event))
    ]

    # Starting threads
    for thread in threads:
        thread.start()

    # Waiting for all threads to complete before exiting the main thread
    for thread in threads:
        thread.join()

    print("Disconnecting from STM")
    STM.disconnect()

    print("Task completed.")
