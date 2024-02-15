# import a utility function for loading Roboflow models
from inference import get_roboflow_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2
from dotenv import load_dotenv
import os
 
# Load environment variables from .env file from relative path
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(dotenv_path)
load_dotenv(dotenv_path)
# Access the API key
API_KEY = os.getenv('ROBOFLOW_API_KEY')
print(API_KEY)
# load a pre-trained yolov8n model
model = get_roboflow_model(model_id="2024-grp-16-image-rec/5",api_key=API_KEY)


def predict_id(image_file_path):
    image = cv2.imread(image_file_path)

    # run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
    results = model.infer(image)

    # print results
    print()
    print(results)

    #show annotation
    show_annotation(image,results)

    # extract class name
    class_name = None
    largest_size = -1
    for result in results:  # If 'results' is not a list, remove this loop
        for prediction in result.predictions:
            print(prediction)
            if largest_size == -1 or max(prediction.width,prediction.height) > largest_size:
                largest_size = max(prediction.width,prediction.height)
                class_name = prediction.class_name

    if class_name:
        print("class_name = "+class_name)
    else:
        print("class_name = None")

    return class_name

def show_annotation(image,results):
    # # load the results into the supervision Detections api
    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

    # create supervision annotators
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # annotate the image with our inference results
    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections)

    # Display the annotated image
    cv2.imshow("Annotated Image", annotated_image)
    cv2.waitKey(3000)  # Display the image for 3 seconds (3000 milliseconds)
    cv2.destroyAllWindows()  # Close all OpenCV windows after the wait time


image_file_path = "images/image_test2.jpg"
predict_id(image_file_path)