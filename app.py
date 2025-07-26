from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- Dashboard Route ----------
@app.route('/summary', methods=['GET'])
def dashboard():
    try:
        api_url = 'https://4e0cb01f9def.ngrok-free.app/summary'
        response = requests.get(api_url)
        response.raise_for_status()

        api_data = response.json()
        summary = api_data.get("summary", {})

        return render_template("dashboard.html", summary=summary)

    except requests.exceptions.RequestException as e:
        return f"Error fetching data from API: {e}", 500

# ---------- Upload Page Route ----------
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    files = {
        'file': (image_file.filename, image_file.stream, image_file.content_type)
    }

    try:
        response = requests.post(
            'https://4e0cb01f9def.ngrok-free.app/upload-receipt',
            files=files
        )

        if response.status_code == 200:
            return jsonify({"message": "Submitted Successfully", "response": response.json()})
        else:
            return jsonify({
                "error": "OCR API error",
                "status_code": response.status_code,
                "details": response.text
            }), response.status_code
    except Exception as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

# ---------- Chat Routes ----------
@app.route('/chat', methods=['GET'])
def chat_page():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    question = data.get("question", "")

    try:
        response = requests.post(
            "https://4e0cb01f9def.ngrok-free.app/ask",
            json={"question": question}
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({"answer": result.get("answer", "No answer provided")})
        else:
            return jsonify({"answer": "Error: Chatbot API failed."}), 500
    except Exception as e:
        return jsonify({"answer": f"Request error: {str(e)}"}), 500


# ---------- Run the Flask App ----------
if __name__ == '__main__':
    app.run(debug=True)
