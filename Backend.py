from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS 
from dotenv import load_dotenv  
import os
import webbrowser
import threading
import google.generativeai as genai 
import logging  

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

# Open browser once
def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):  
        webbrowser.open("http://127.0.0.1:5000/")

# Run Flask
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()  
    app.run(debug=os.getenv("FLASK_DEBUG", "false").strip().lower() in ["1", "true"])  
