from http import HTTPStatus
import json
import os
from dashscope import Application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
API_KEY = os.getenv('DASHSCOPE_API_KEY')
APP_ID = os.getenv('DASHSCOPE_APP_ID')

def handler(request):
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
        body = json.loads(request.body)
        
        # Verify environment variables
        if not API_KEY or not APP_ID:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": True,
                    "message": "Missing API credentials"
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        # Verify request data
        if not body or 'prompt' not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": True,
                    "message": "Missing prompt in request"
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        # Call AI API
        try:
            response = Application.call(
                api_key=API_KEY,
                app_id=APP_ID,
                prompt=body['prompt']
            )

            if response.status_code != HTTPStatus.OK:
                return {
                    "statusCode": response.status_code,
                    "body": json.dumps({
                        "error": True,
                        "message": getattr(response, 'message', 'API call failed'),
                        "request_id": getattr(response, 'request_id', None),
                        "code": response.status_code
                    }),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                }

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "output": {
                        "text": response.output.text
                    }
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        except Exception as api_error:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": True,
                    "message": f"API call failed: {str(api_error)}"
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": True,
                "message": f"Server error: {str(e)}"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        } 