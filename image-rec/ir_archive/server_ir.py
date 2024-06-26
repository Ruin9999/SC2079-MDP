import socket
from datetime import datetime
from predict import Predictor
from id_mapping import mapping
from show_annotation import start_annotation_process
from multiprocessing import Process, Queue

# Change to your laptop host ip when connected to RPI Wifi
# use ipconfig to find your laptop host ip 
#HOST = '192.168.151.23' #Aaron Laptop (NTUSECURE)
HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
#HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
#HOST = '192.168.80.27'  #Cy Laptop (RPICy)

PORT = 2030 
HEADER_SIZE = 10        # Number of bytes to use for the header
BUFFER_SIZE = 4096      # Standard size for buffer

def receive_file(conn):
    try:
        # Receive the header containing the file name size
        file_name_size = conn.recv(HEADER_SIZE)
        if not file_name_size:
            return None  # Connection closed or error

        file_name_size = int(file_name_size.decode().strip())
        # Receive the file name
        file_name = conn.recv(file_name_size).decode()

        # Receive the header containing the direction size
        direction_size = conn.recv(HEADER_SIZE)
        if not direction_size:
            return None  # Connection closed or error

        direction_size = int(direction_size.decode().strip())
        # Receive the direction
        direction = conn.recv(direction_size).decode()

        
        # Receive the header containing the image size
        img_size = conn.recv(HEADER_SIZE)
        if not img_size:
            return None  # Connection closed or error
        
        img_size = int(img_size.decode().strip())
        data = bytearray()

        # Receive the file data
        while len(data) < img_size:
            packet = conn.recv(min(BUFFER_SIZE, img_size - len(data)))
            if not packet:
                break
            data.extend(packet)

        # file_path = f"images\{file_name}"
        #file_path = f"C:\\Users\\CY\\Documents\\NTU Year 3 Sem 2\\SC2079 - MDP\\Repo\\image-rec\\images\\{file_name}"
        file_path = "C:\\Users\\draco\\Desktop\\github\\SC2079-MDP\\image-rec\\images\\{file_name}"
        # Save the file data to a file with the received name
        with open(file_path, 'wb') as file:
            file.write(data)
        return file_path, direction

    except Exception as e:
        print(f"Error receiving file: {e}")
        return None, None  # Return None values indicating an error occurred

def start_server(show_annotation_queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
        predictor = Predictor()

        while True:  # Keep server running to accept multiple connections
            conn, addr = s.accept()
            with conn:
                startTime = datetime.now()
                print(f"\nConnected by {addr}")
                result = receive_file(conn)  # Receive the result as a single variable
                endTime = datetime.now()
                totalTime = (endTime - startTime).total_seconds()
                print(f"Time taken for Receiving Image = {totalTime} s")

                if result:  # Check if result is not None
                    file_path, direction = result  # Now unpack safely
                    if file_path and direction:
                        print("File received and saved successfully.")
                        print(f"Direction received: {direction}")

                        startTime = datetime.now()
                        class_name, results = predictor.predict_id(file_path)  # Perform prediction
                        show_annotation_queue.put((file_path, results))

                        class_id = str(mapping.get(class_name, -1))  # Use .get() to handle None
                        print(f"Predicted ID: {class_id}")
                        endTime = datetime.now()
                        totalTime = (endTime - startTime).total_seconds()
                        print(f"Time taken for Predicting Image = {totalTime} s")

                        # Send back prediction ID to client
                        conn.sendall(class_id.encode('utf-8'))
                    else:
                        print("Failed to receive file.")
                else:
                    print("Failed to receive file or connection error.")



if __name__ == "__main__":
    show_annotation_queue = Queue()

    process1 = Process(target=start_server, args=(show_annotation_queue,))
    process2 = Process(target=start_annotation_process, args=(show_annotation_queue,))
    
    process1.start()
    process2.start()

    process1.join()
    process2.join()
    
