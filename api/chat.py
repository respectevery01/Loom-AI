from http import HTTPStatus
import json
import os
import dashscope
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables with correct names
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

# Initialize Flask app
app = Flask(__name__)

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def handler():
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

    try:
        # Get request body
        try:
            body = request.get_json()
            print(f"Parsed request body: {body}")
        except Exception as body_error:
            print(f"Error parsing request body: {str(body_error)}")
            error_response = jsonify({
                "error": True,
                "message": f"Invalid request body: {str(body_error)}"
            })
            error_response.headers['Access-Control-Allow-Origin'] = '*'
            return error_response, 400
        
        # Verify environment variables
        if not DASHSCOPE_API_KEY:
            error_msg = "Missing API credentials"
            print(f"Error: {error_msg}")
            error_response = jsonify({
                "error": True,
                "message": error_msg
            })
            error_response.headers['Access-Control-Allow-Origin'] = '*'
            return error_response, 500

        # Verify request data
        if not body or 'prompt' not in body:
            error_msg = "Missing prompt in request"
            print(f"Error: {error_msg}")
            error_response = jsonify({
                "error": True,
                "message": error_msg
            })
            error_response.headers['Access-Control-Allow-Origin'] = '*'
            return error_response, 400

        # Call AI API
        try:
            print(f"Calling API with prompt: {body['prompt']}")
            response = dashscope.Generation.call(
                model="qwen-max",
                api_key=DASHSCOPE_API_KEY,
                prompt=body['prompt']
            )
            
            print(f"API Response status: {response.status_code}")

            if response.status_code != HTTPStatus.OK:
                error_msg = {
                    "error": True,
                    "message": getattr(response, 'message', 'API call failed'),
                    "request_id": getattr(response, 'request_id', None),
                    "code": response.status_code
                }
                print(f"API Error: {error_msg}")
                error_response = jsonify(error_msg)
                error_response.headers['Access-Control-Allow-Origin'] = '*'
                return error_response, response.status_code

            result = {
                "output": {
                    "text": response.output.text
                }
            }
            print(f"Success response: {result}")
            success_response = jsonify(result)
            success_response.headers['Access-Control-Allow-Origin'] = '*'
            return success_response, 200

        except Exception as api_error:
            error_msg = f"API call failed: {str(api_error)}"
            print(f"Error: {error_msg}")
            error_response = jsonify({
                "error": True,
                "message": error_msg
            })
            error_response.headers['Access-Control-Allow-Origin'] = '*'
            return error_response, 500

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        error_response = jsonify({
            "error": True,
            "message": error_msg
        })
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response, 500 