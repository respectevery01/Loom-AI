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

# Debug print for environment variables
print(f"API_KEY exists: {bool(API_KEY)}")
print(f"APP_ID exists: {bool(APP_ID)}")

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
        print(f"Static file error: {str(e)}")
        return str(e), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        print("Received request:", request.json)

        if not API_KEY or not APP_ID:
            error_msg = {
                'error': True,
                'message': 'Missing API credentials. Please check your .env file.'
            }
            print("Error:", error_msg)
            return jsonify(error_msg), 500

        data = request.json
        if not data or 'prompt' not in data:
            error_msg = {
                'error': True,
                'message': 'Missing prompt in request'
            }
            print("Error:", error_msg)
            return jsonify(error_msg), 400

        try:
            print(f"Calling API with prompt: {data['prompt']}")
            response = Application.call(
                api_key=API_KEY,
                app_id=APP_ID,
                prompt=data['prompt']
            )
            
            print("API Response status:", response.status_code)

            if response.status_code != HTTPStatus.OK:
                error_msg = {
                    'error': True,
                    'message': getattr(response, 'message', 'API call failed'),
                    'request_id': getattr(response, 'request_id', None),
                    'code': response.status_code
                }
                print("API Error:", error_msg)
                return jsonify(error_msg), response.status_code
            
            result = {
                'output': {
                    'text': response.output.text
                }
            }
            print("Success response:", result)
            return jsonify(result)

        except Exception as api_error:
            error_msg = {
                'error': True,
                'message': f'API call failed: {str(api_error)}'
            }
            print("API Error:", error_msg)
            return jsonify(error_msg), 500

    except Exception as e:
        error_msg = {
            'error': True,
            'message': f'Server error: {str(e)}'
        }
        print("Server Error:", error_msg)
        return jsonify(error_msg), 500

if __name__ == '__main__':
    if not API_KEY or not APP_ID:
        print("\nWarning: Missing API credentials in .env file!")
        print("Make sure you have DASHSCOPE_API_KEY and DASHSCOPE_APP_ID set in your .env file.")
        print("Current environment variables:")
        print(f"DASHSCOPE_API_KEY exists: {bool(API_KEY)}")
        print(f"DASHSCOPE_APP_ID exists: {bool(APP_ID)}\n")
    
    print("Starting development server...")
    app.run(debug=True, port=5000) 