from http import HTTPStatus
import json
import os
import dashscope
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables with correct names
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

# Debug print
print(f"Environment variables loaded:")
print(f"DASHSCOPE_API_KEY exists: {bool(DASHSCOPE_API_KEY)}")

def handle_options():
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    }

def handle_error(status_code, message):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "error": True,
            "message": message
        })
    }

def handle(request):
    # Handle OPTIONS request
    if request.get('method', '') == 'OPTIONS':
        return handle_options()

    try:
        # Get request body
        try:
            body = json.loads(request.get('body', '{}'))
            print(f"Parsed request body: {body}")
        except Exception as body_error:
            print(f"Error parsing request body: {str(body_error)}")
            return handle_error(400, f"Invalid request body: {str(body_error)}")
        
        # Verify environment variables
        if not DASHSCOPE_API_KEY:
            error_msg = "Missing API credentials"
            print(f"Error: {error_msg}")
            return handle_error(500, error_msg)

        # Verify request data
        if not body or 'prompt' not in body:
            error_msg = "Missing prompt in request"
            print(f"Error: {error_msg}")
            return handle_error(400, error_msg)

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
                return {
                    "statusCode": response.status_code,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps(error_msg)
                }

            result = {
                "output": {
                    "text": response.output.text
                }
            }
            print(f"Success response: {result}")
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(result)
            }

        except Exception as api_error:
            error_msg = f"API call failed: {str(api_error)}"
            print(f"Error: {error_msg}")
            return handle_error(500, error_msg)

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        return handle_error(500, error_msg) 