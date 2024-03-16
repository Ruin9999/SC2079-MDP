from flask import Flask, request, jsonify
import os
import importlib.util
from datetime import datetime
from predict import Predictor
from id_mapping import mapping
from show_annotation import start_annotation_process
from multiprocessing import Process, Queue

app = Flask(__name__)

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rpi', 'config'))
config_path = os.path.join(config_dir, 'PC_CONFIG.py')
spec = importlib.util.spec_from_file_location("PC_CONFIG", config_path)
PC_CONFIG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PC_CONFIG)

HOST = PC_CONFIG.HOST
PORT = PC_CONFIG.IMAGE_REC_PORT
UPLOAD_FOLDER =  PC_CONFIG.FILE_DIRECTORY + "image-rec\\images\\"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_file(file_path, direction, show_annotation_queue):
    predictor = Predictor()
    print("File received and saved successfully.")
    print(f"Direction received: {direction}")

    startTime = datetime.now()
    class_name, results, detection_id = predictor.predict_id(file_path)  # Perform prediction
    show_annotation_queue.put((file_path, results, detection_id))
    class_id = str(mapping.get(class_name, -1))
    endTime = datetime.now()
    totalTime = (endTime - startTime).total_seconds()
    print(f"Predicted ID: {class_id}")
    print(f"Time taken for Predicting Image = {totalTime} s")
    return class_id

@app.route('/status', methods=['GET'])
def server_status():
    return jsonify({'status': 'OK'})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    direction = request.form['direction']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = os.path.basename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file and predict
        class_id = process_file(file_path, direction, show_annotation_queue)
        return jsonify({'message': 'File successfully uploaded', 'predicted_id': class_id}), 200

@app.route('/display_stitched', methods=['POST'])
def display_stitched():
    show_annotation_queue.put(("STOP",))
    return jsonify({'display_stitched': 'OK'})

if __name__ == '__main__':
    show_annotation_queue = Queue()
    process = Process(target=start_annotation_process, args=(show_annotation_queue,))
    process.start()
    
    print()
    print(f"UPLOAD FOLDER: {UPLOAD_FOLDER}")
    try:
        app.run(host=HOST, port=PORT, debug=True)
    except:
        print('Unable to Connect to PC_CONFIG Host and Port. Switching to 0.0.0.0:4000.')
        app.run(host='0.0.0.0', port=4000, debug=True)
     
    process.join()
