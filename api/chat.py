from http import HTTPStatus
import json
import os
import dashscope
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables with correct names
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_APP_ID = os.getenv('DASHSCOPE_APP_ID')

# Debug print
print(f"Environment variables loaded:")
print(f"DASHSCOPE_API_KEY exists: {bool(DASHSCOPE_API_KEY)}")
print(f"DASHSCOPE_APP_ID exists: {bool(DASHSCOPE_APP_ID)}")

def handler(request):
    print(f"Received request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    
    # Enable CORS
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return {"statusCode": 200, "headers": headers}

    try:
        # Get request body
        try:
            # Try different ways to get the request body
            if hasattr(request, 'json'):
                print("Using request.json")
                body = request.json
            elif hasattr(request, 'body'):
                print("Using request.body")
                if isinstance(request.body, str):
                    body = json.loads(request.body)
                else:
                    body = json.loads(request.body.decode('utf-8'))
            else:
                print("No recognized body format")
                body = {}
            
            print(f"Parsed request body: {body}")
        except Exception as body_error:
            print(f"Error parsing request body: {str(body_error)}")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": True,
                    "message": f"Invalid request body: {str(body_error)}"
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        
        # Verify environment variables
        if not DASHSCOPE_API_KEY or not DASHSCOPE_APP_ID:
            error_msg = "Missing API credentials"
            print(f"Error: {error_msg}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": True,
                    "message": error_msg
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        # Verify request data
        if not body or 'prompt' not in body:
            error_msg = "Missing prompt in request"
            print(f"Error: {error_msg}")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": True,
                    "message": error_msg
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

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
                    "body": json.dumps(error_msg),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                }

            result = {
                "output": {
                    "text": response.output.text
                }
            }
            print(f"Success response: {result}")
            return {
                "statusCode": 200,
                "body": json.dumps(result),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        except Exception as api_error:
            error_msg = f"API call failed: {str(api_error)}"
            print(f"Error: {error_msg}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": True,
                    "message": error_msg
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": True,
                "message": error_msg
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        } 