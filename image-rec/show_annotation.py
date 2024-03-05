import cv2
import supervision as sv
import time

def start_annotation_process(queue):
    while True:
        if not queue.empty():
            image_file_path, results = queue.get()
            image = cv2.imread(image_file_path)
            show_annotation(image, results)

def show_annotation(image, results):
    # Load the results into the supervision Detections API
    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

    # Create supervision annotators
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    # Annotate the image with inference results
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    
    # Display the annotated image
    cv2.imshow("Annotated Image", annotated_image)
    cv2.waitKey(3000)  # Display the image for 3 seconds
    cv2.destroyAllWindows()  # Close all OpenCV windows
