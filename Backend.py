from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS 
from dotenv import load_dotenv  
import os
import webbrowser
import threading
import google.generativeai as genai 
import logging  
from werkzeug.utils import secure_filename  # <--- Import for secure file saving

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__, static_folder="dist")  
CORS(app)  

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Set upload folder for images
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')  # Ensure uploads directory is within 'dist'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create upload directory if it doesn't exist

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory("dist", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("dist", path)

# Chatbot API
@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Image upload API
@app.route("/api/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return jsonify({"message": "File successfully uploaded", "filename": filename}), 200

# Open browser once
# def open_browser():
#     if not os.environ.get("WERKZEUG_RUN_MAIN"):  
#         webbrowser.open("http://127.0.0.1:5000/") 

# Run Flask
if __name__ == "__main__":
   # threading.Timer(1.5, open_browser).start()  
    app.run(debug=os.getenv("FLASK_DEBUG", "false").strip().lower() in ["1", "true"]) 
