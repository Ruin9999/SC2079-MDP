from threading import Lock
from picamera import PiCamera
from time import sleep
from datetime import datetime

# Initialize the camera lock
camera_lock = Lock()

def take_pic():
    with camera_lock:
        with PiCamera() as camera:
            camera.resolution = (640, 640)
            sleep(2)  # Camera warm-up time

            now = datetime.now()
            folder_path = "images/"
            image_name = now.strftime("image_%Y-%m-%d_%H-%M-%S.jpg")
            image_path = folder_path + image_name

            camera.capture(image_path)
            print(f"Image captured and saved at {image_path}")

            return image_path
