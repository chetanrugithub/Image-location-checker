import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])  
def analyze():
    uploaded_files = request.files.getlist("images")

    # Save uploaded images
    image_paths = []
    for file in uploaded_files:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        image_paths.append(path)

    # Load Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare input for Gemini
    prompt = "Compare these images and tell me if they are from the same location or not or Real or Fake. Give Yes/No and explain why."
    parts = [prompt]

    # Add image binary data
    for img in image_paths:
        with open(img, "rb") as f:
            parts.append({"mime_type": "image/jpeg", "data": f.read()})

    # Get responseS
    response = model.generate_content(parts)

    return jsonify({"analysis": response.text})

if __name__ == "__main__":
    app.run(debug=True)
