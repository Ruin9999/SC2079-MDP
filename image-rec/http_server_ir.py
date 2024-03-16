from flask import Flask, request, jsonify
import os
from datetime import datetime
from predict import Predictor
from id_mapping import mapping
from show_annotation import start_annotation_process
from multiprocessing import Process, Queue
from show_stitched import showAnnotatedStitched

app = Flask(__name__)



UPLOAD_FOLDER = "C:\\Users\\CY\\Documents\\NTU Year 3 Sem 2\\SC2079 - MDP\\Repo\\image-rec\\images\\"
# UPLOAD_FOLDER = "C:\\Users\\draco\\Desktop\\github\\SC2079-MDP\\image-rec\\images"
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
    
    # HOST = '192.168.16.22' #Aaron Laptop (MDPGrp16)
    HOST = '192.168.16.11' #Cy Laptop (MDPGrp16)
    #HOST = '192.168.80.27'  #Cy Laptop (RPICy)
    # app.run(host='0.0.0.0', port=4000, debug=True)
    print()

    app.run(host=HOST, port=2030, debug=True)
    
    process.join()
