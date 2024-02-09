from picamera import PiCamera
from time import sleep
from datetime import datetime


def take_pic():
    # Create an object for the PiCamera
    camera = PiCamera()

    # Optional: Set camera resolution. 640 x 640
    camera.resolution = (640, 640)

    # Give the camera some warm-up time
    sleep(2)

    # Get the current datetime
    now = datetime.now()
    folder_path = "images/"
    image_name = now.strftime("image_%Y-%m-%d_%H-%M-%S.jpg")
    image_path = folder_path + image_name
    print(image_path)

    # Capture to a file
    camera.capture(image_path)
    print("Image captured and saved")

    return image_path



