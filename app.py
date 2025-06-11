from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
import tensorflow as tf

# Setup Flask app
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="ML_models/waste_classifier_resnet50.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Labels and descriptions
labels = ["bio", "nonbio"]
descriptions = {
    "bio": "Biodegradable waste such as food scraps, paper, and natural materials.",
    "nonbio": "Non-biodegradable waste like plastics, metals, and synthetic materials."
}

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))  # adjust size if your model requires a different one
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # batch dimension
    return img_array

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image file part in the request"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"message": "No selected image file"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(filepath)

    # Preprocess and predict
    input_data = preprocess_image(filepath)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    predicted_index = int(np.argmax(output_data))
    predicted_label = labels[predicted_index]
    description = descriptions[predicted_label]

    return jsonify({
        "message": "Image received and processed.",
        "prediction": predicted_label,
        "description": description,
        "filename": image_file.filename
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
