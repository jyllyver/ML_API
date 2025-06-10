# Import necessary modules from Flask
from flask import Flask, request, jsonify
from flask_cors import CORS # Import Flask-CORS
import os

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes.
# In a production environment, you might want to restrict this to specific origins (e.g., CORS(app, origins="http://yourfrontend.com")).
# For development, allowing all origins ('*') is convenient.
CORS(app)

# Define the folder where uploaded images will be saved
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) # Create the folder if it doesn't exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a route that will handle image uploads
# This route will only accept POST requests.
@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Check if the 'image' file is present in the request.
    # The 'image' key is the name of the input field in the form or the key
    # in the multipart/form-data request body that contains the file.
    if 'image' not in request.files:
        # If no file is found with the 'image' key, return an error message.
        return jsonify({"message": "No image file part in the request"}), 400

    image_file = request.files['image']

    # If the user does not select a file, the browser submits an empty file
    # without a filename. We should handle this case.
    if image_file.filename == '':
        return jsonify({"message": "No selected image file"}), 400

    # If an image file is present and has a filename, proceed to save it.
    if image_file:
        # Securely save the file. For a real application, you might want
        # to use `werkzeug.utils.secure_filename` to sanitize the filename.
        # For this example, we'll just save it directly.
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(filepath)

        # Return a success message indicating the image was received.
        # You can include the filename and path for confirmation.
        return jsonify({
            "message": "Image received successfully!",
            "filename": image_file.filename,
            "filepath": filepath
        }), 200 # HTTP status code 200 for OK

# Main entry point for the Flask application.
# This will run the development server.
if __name__ == '__main__':
    # Run the app on host '0.0.0.0' to make it accessible from other devices
    # on the network (useful for testing on different machines) and port 5000.
    # debug=True allows for automatic reloads on code changes and provides
    # a debugger. Set to False in production.
    app.run(host='0.0.0.0', port=5000, debug=True)
