import time
import queue
import threading
import socket
import json
from environment import Environment, Obstacle
import os
from takepic import take_pic

from server_bt import BluetoothServer
from client_algo import AlgorithmClient
from client_ir import ImageRecognitionClient
from STM32 import STM32Server

def startBTServer(bt_queue, running_flag, ir_event):
    print("Connecting to Android")
    while running_flag[0]:
        if not bt_queue.empty():
            msg = bt_queue.get()
            command, *optional_parts = msg  # Correct way to unpack

            print(f"\nmsg sent to android: {msg}")
            print(f"command: {command}")

            if command == "IR":
                print(f"IR msg: {msg}")
                if optional_parts:  # This checks if there are any optional parts
                    # optional_parts is a list, handle accordingly
                    number_part, predict_id = optional_parts
                    print(f"IR optional parts: Number part = {number_part}, Predict ID = {predict_id}")
                    ir_event.set()
            elif command == "FIN":
                print(f"FIN msg: {msg}\n")
                running_flag[0] = False
            else:
                # Handle other commands or continue loop
                continue
    print("Disconnecting from Android Bluetooth")

    # bt_server = BluetoothServer()
    # try:
    #     while True:
    #         data = bt_server.receive_data()
    #         bt_server.send_data("START")
    #         time.sleep(32)

    #         #if start send to algo

    #         if not bt_queue.empty():
    #             predict_id = bt_queue.get()
    #             bt_server.send(predict_id)

    # except KeyboardInterrupt:
    #     bt_server.close_connection()


def startAlgoClient(algo_queue, ir_queue, stm32_queue, bt_queue, running_flag, ir_event, stm32_event):
    HOST = '192.168.80.27'
    PORT = 2040
    client = AlgorithmClient(HOST,PORT)
    print("Connecting to Algo Server")
    client.connect()

    #test - assume that msg received from android and is put into queue
    algo_queue.put(1)

    while running_flag[0]:
        if not algo_queue.empty():
            algo_queue_msg = algo_queue.get()

            # Example object to send
            env = {"size_x": 100, "size_y": 100, "robot_x": 10, "robot_y": 10, "robot_direction": 'N'}  
            response_received = None
            try_count = 1

            while not response_received and try_count <= 3:
                response_received = client.send(env)
                try_count += 1

            if response_received:
                print("Extracting the data from response:")
                commands = response_received["commands"] 
                print("Commands:", commands,"\n")

                substring = "SNAP"
                if commands:
                    for command in commands:
                        ir_event.wait()
                        stm32_event.wait()
                        if substring in command:
                            ir_event.clear()
                            number_part = command[len(substring):]
                            ir_queue.put((substring,number_part))
                        elif command == "FIN":
                            bt_queue.put((command,))
                        else:
                            stm32_event.clear()
                            stm32_queue.put(command)       

    print("Disconnecting from Algo Server")
    client.disconnect()


def startIRClient(ir_queue, bt_queue, running_flag, ir_event):
    HOST = '192.168.80.27'
    PORT = 2030
    client = ImageRecognitionClient(HOST,PORT)  # Optionally pass host and port
    print("Connecting to Image Rec Server")
    client.connect()

    while running_flag[0]:
        if not ir_queue.empty():
            (substring,number_part) = ir_queue.get()
            print(f"substring is {substring}")
            print(f"Taking a photo for obstacle no {number_part}")
            file_path = take_pic()
            predict_id = client.send_file(file_path)
            bt_queue.put(("IR", number_part, predict_id))

    print("Disconnecting from Image Rec Server")
    client.disconnect()

def startSTMServer(stm32_queue, running_flag, stm32_event):
    print("Connecting to STM")

    while running_flag[0]:
        if not stm32_queue.empty():
            msg = stm32_queue.get()
            print(f"stm32 queue msg = {msg}\n")
            stm32_event.set()

    print("Disconnecting from STM")
    # #displacement = ["center,0,reverse,15", "left,90,forward,5","right,180,forward,5"]
    # STM = STM32()
    # STM.connect()
    # STM.send("0FW090")

    # received_msg = None

    # while(True):
    #     received_msg = STM.recv()
    #     if(received_msg):
    #         break

    # STM.disconnect()


if __name__ == "__main__":
    # Queues for communication between threads
    bt_queue = queue.Queue()
    algo_queue = queue.Queue()
    ir_queue = queue.Queue()
    stm32_queue = queue.Queue()

    # Events for ordering of threads (need to wait for each command from algo)
    # event should be cleared as early as possible (eg clearing before putting into queue)
    # event should be set only when all the corresponding step for a task have been completed
    ir_event = threading.Event()
    stm32_event = threading.Event()
    # no need to wait at the start, so intital event is set
    ir_event.set()
    stm32_event.set()

    # Flag to control the execution of threads
    running_flag = [True]

    # Creating threads for each task
    threads = [
        threading.Thread(target=startBTServer, args=(bt_queue, running_flag, ir_event)),
        threading.Thread(target=startAlgoClient, args=(algo_queue, ir_queue, stm32_queue, bt_queue, running_flag, ir_event, stm32_event)),
        threading.Thread(target=startIRClient, args=(ir_queue, bt_queue, running_flag, ir_event)),
        threading.Thread(target=startSTMServer, args=(stm32_queue, running_flag, stm32_event))
    ]

    # Starting threads
    for thread in threads:
        thread.start()

    # Waiting for all threads to complete before exiting the main thread
    for thread in threads:
        thread.join()

    print("Task completed.")

    