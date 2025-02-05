from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from http import HTTPStatus
from dashscope import Application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Get environment variables
API_KEY = os.getenv('DASHSCOPE_API_KEY')
APP_ID = os.getenv('DASHSCOPE_APP_ID')

if not API_KEY or not APP_ID:
    raise ValueError("Missing required environment variables. Please check .env file or environment settings.")

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=data['prompt']
        )

        if response.status_code != HTTPStatus.OK:
            return jsonify({
                'error': True,
                'message': response.message,
                'request_id': response.request_id,
                'code': response.status_code
            }), response.status_code
        
        return jsonify({
            'output': {
                'text': response.output.text
            }
        })

    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)