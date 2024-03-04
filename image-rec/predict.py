import cv2
import os
from dotenv import load_dotenv
from inference import get_roboflow_model
import supervision as sv

class Predictor:
    def __init__(self):
        # Load environment variables from .env file from relative path
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path)
        # Access the API key
        self.api_key = os.getenv('ROBOFLOW_API_KEY')
        # Load a pre-trained yolov8n model
        self.model = get_roboflow_model(model_id="2024-grp-16-image-rec/8", api_key=self.api_key)

    def predict_id(self, image_file_path):
        # Load the image
        image = cv2.imread(image_file_path)

        # Run inference on the image
        results = self.model.infer(image)

        # Print results
        print(results)
        # Show annotation
        self.show_annotation(image, results)

        # Extract class name
        class_name, largest_size = None, -1
        for result in results:  # Assuming 'results' is a list
            for prediction in result.predictions:
                print(prediction)
                if largest_size == -1 or max(prediction.width, prediction.height) > largest_size:
                    largest_size = max(prediction.width, prediction.height)
                    class_name = prediction.class_name

        if class_name:
            print("class_name = " + class_name)
        else:
            print("class_name = None")

        return class_name

    def show_annotation(self, image, results):
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

if __name__ == "__main__":
    # Example usage
    predictor = Predictor()
    # Specify the path to your image
    image_file_path = "images/image_test2.jpg"
    # Predict and display the class name
    predictor.predict_id(image_file_path)
