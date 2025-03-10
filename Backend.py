from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import google.generativeai as genai

# ✅ Configure API Key
genai.configure(api_key="AIzaSyDGvR_OAz0iGn69q-DYZafJFNeASEGVsS4")

# ✅ Initialize the model
MODEL_ID = "gemini-1.5-pro"  # Use a valid model like gemini-1.5-pro
chat_instance = genai.GenerativeModel(MODEL_ID)

# ✅ Start a chat session to maintain history
chat_session = chat_instance.start_chat(history=[])

# ✅ Function to chat with the model and maintain conversation history
def chat_with_model(prompt):
    response = chat_session.send_message(prompt)  # Uses chat history
    return response.text  # ✅ Ensure it returns text, not an object

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__, static_folder="dist")
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# ✅ Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory("dist", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("dist", path)

# ✅ Chatbot API with session continuity
@app.route("/api/chat", methods=["POST"])
def chat_api():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response_text = chat_with_model(user_message)  # ✅ Maintains conversation history
        return jsonify({"response": response_text})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# ✅ Run Flask
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").strip().lower() in ["1", "true"])
