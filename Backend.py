from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import google.generativeai as genai
import openai
import requests
import PyPDF2
import pandas as pd
import docx

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__, static_folder="dist")
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Configure API Key
genai.configure(api_key="AIzaSyDGvR_OAz0iGn69q-DYZafJFNeASEGVsS4")
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in .env

# ICD-10 API Credentials
ICD10_CLIENT_ID = os.getenv("ICD10_CLIENT_ID")
ICD10_CLIENT_SECRET = os.getenv("ICD10_CLIENT_SECRET")

# Initialize the model
MODEL_ID = "gemini-2.0-flash-exp"
chat_instance = genai.GenerativeModel(MODEL_ID)

# Start a chat session to maintain history
chat_session = chat_instance.start_chat(history=[])

def get_chat():
    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=" You are an AI medical assistant integrated into MedInsight, an AI-powered medical report analysis system. Your responses must be concise, accurate, and focused on medical insights. When analyzing medical reports, provide clear explanations of key findings, diagnoses, and recommendations in simple medical terms. Avoid unnecessary details and ensure clarity for both medical professionals and patients. Important: Do not use asterisks (*) in the response. List more key points when summarizing findings, diagnoses, and recommendations. Ensure structured, well-formatted output without markdown symbols.",
            temperature=0.5,
        ),
    )
    return chat

# Function to chat with the model and maintain conversation history
def chat_with_model(prompt):
    response = chat_session.send_message(prompt)  # Uses chat history
    return response.text

# Function to extract text from files
def extract_text(file_path):
    extracted_text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                extracted_text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
        extracted_text = df.to_string()
    return extracted_text

# Function to analyze text using GPT-4
def analyze_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical AI assistant. Extract key medical data, summarize results, and classify into normal, alert, or consult doctor."},
            {"role": "user", "content": text},
        ]
    )
    return response["choices"][0]["message"]["content"]

# Function to fetch ICD-10 disease classification
def get_icd10_classification(medical_terms):
    url = "https://icd10api.com/api/lookup"
    headers = {"Content-Type": "application/json"}
    auth = (ICD10_CLIENT_ID, ICD10_CLIENT_SECRET)
    response = requests.post(url, json={"query": medical_terms}, auth=auth)
    return response.json() if response.status_code == 200 else {}

# Analyze API Route
@app.route("/analyze", methods=["POST"])
def analyze_report():
    data = request.json
    file_path = data.get("file_path")
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    extracted_text = extract_text(file_path)
    if not extracted_text:
        return jsonify({"error": "No text extracted from document"}), 400

    analysis_result = analyze_text(extracted_text)
    icd10_result = get_icd10_classification(extracted_text)
    
    return jsonify({
        "message": "Analysis complete",
        "analysis": analysis_result,
        "icd10_classification": icd10_result,
    }), 200

# Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory("dist", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("dist", path)

# Chatbot API with session continuity
@app.route("/api/chat", methods=["POST"])
def chat_api():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    try:
        response_text = chat_with_model(user_message)
        return jsonify({"response": response_text})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# File Upload API
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

# Run Flask
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").strip().lower() in ["1", "true"])
