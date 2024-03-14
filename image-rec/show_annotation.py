import cv2
import supervision as sv
import time
import os
from id_mapping import mapping
from multiprocessing import Process, Queue
from predict import Predictor
from show_stitched import showAnnotatedStitched
import shutil
from datetime import datetime

def start_annotation_process(queue):
    image_count = 0
    file_dir = f"C:\\Users\\CY\\Documents\\NTU Year 3 Sem 2\\SC2079 - MDP\\Repo\\image-rec\\annotated_images\\"
    archive_directory_content(file_dir)

    while True:
        if not queue.empty():

            item = queue.get()  # Wait for an item from the queue
            if item == "STOP":  # Check for the termination signal
                print("Stopping annotation process.")
                break  # Exit the loop to end the process
            image_file_path, results = item
            image = cv2.imread(image_file_path)
            image_count += 1
            show_annotation(image, results, image_count)

def archive_directory_content(directory_path):
    # Moves files with the specified extension from the given directory to an archive directory,
    # except for files named .gitkeep.

    archive_dir="C:\\Users\\CY\\Documents\\NTU Year 3 Sem 2\\SC2079 - MDP\\Repo\\image-rec\\annotated_archive"
    file_extension=".jpg"
    os.makedirs(archive_dir, exist_ok=True)  # Create the archive directory if it doesn't exist
    
    for filename in os.listdir(directory_path):
        if filename.endswith(file_extension) and filename != ".gitkeep":
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_filename = f"{filename.rsplit('.', 1)[0]}_{timestamp}.{filename.rsplit('.', 1)[1]}"
            src_path = os.path.join(directory_path, filename)
            dest_path = os.path.join(archive_dir, new_filename)
            shutil.move(src_path, dest_path)
            print(f"Moved and renamed: {src_path} to {dest_path}")

def show_annotation(image, results, image_count):
    # Load the results into the supervision Detections API
    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

    class_name = detections.data["class_name"][0]
    class_id = str(mapping.get(class_name, -1))
    updated_label = class_name + ", id=" + class_id
    # updated_label = class_name + ", " + class_id

    # Create supervision annotators
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    # Annotate the image with inference results
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=[updated_label])

    # Save the annotated image with a unique name
    file_name = f"annotated_image{image_count}.jpg"
    file_path = f"C:\\Users\\CY\\Documents\\NTU Year 3 Sem 2\\SC2079 - MDP\\Repo\\image-rec\\annotated_images\\{file_name}"

    cv2.imwrite(file_path, annotated_image)
    print(f"Image saved as {file_path}")

    # Create a named window
    window_name = f"Annotated Image {image_count}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Move the window to a specific position on the screen
    cv2.moveWindow(window_name, 0, 0)

    # Display the saved annotated image
    cv2.imshow(f"Annotated Image {image_count}", annotated_image)
    cv2.waitKey(3000)  # Display the image for 3 seconds
    cv2.destroyAllWindows()  # Close all OpenCV windows


if __name__ == '__main__':
    image_folder_path = r"C:\Users\CY\Documents\NTU Year 3 Sem 2\SC2079 - MDP\Repo\image-rec\sample_images"
    show_annotation_queue = Queue()
    process = Process(target=start_annotation_process, args=(show_annotation_queue,))
    process.start()

    predictor = Predictor()

    # List all .jpg files in the specified directory
    file_path_list = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith('.jpg')]

    for file_path in file_path_list:
        class_name, results = predictor.predict_id(file_path)  # Perform prediction

        print(f"result: {results}")
        show_annotation_queue.put((file_path, results))

    # Send the termination signal to the process
    show_annotation_queue.put("STOP")

    # Wait for the process to finish
    process.join()

    showAnnotatedStitched()