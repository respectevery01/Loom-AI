from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from http import HTTPStatus
from dashscope import Application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Get environment variables
API_KEY = os.getenv('DASHSCOPE_API_KEY')
APP_ID = os.getenv('DASHSCOPE_APP_ID')

# Serve static files
@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    try:
        if os.path.exists(os.path.join('static', path)):
            return send_from_directory('static', path)
        return send_from_directory('static', 'index.html')
    except Exception as e:
        return str(e), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Verify environment variables
        if not API_KEY or not APP_ID:
            return jsonify({
                'error': True,
                'message': 'Missing API credentials'
            }), 500

        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({
                'error': True,
                'message': 'Missing prompt in request'
            }), 400

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

# Development server
if __name__ == '__main__':
    app.run(debug=True, port=5000)