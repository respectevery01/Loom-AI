from http.server import BaseHTTPRequestHandler
import json
import os
from http import HTTPStatus
from dashscope import Application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
API_KEY = os.getenv('DASHSCOPE_API_KEY')
APP_ID = os.getenv('DASHSCOPE_APP_ID')

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            # Print environment variables for debugging (will appear in Vercel logs)
            print(f"API_KEY exists: {bool(API_KEY)}")
            print(f"APP_ID exists: {bool(APP_ID)}")
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Print request data for debugging
            print(f"Received request data: {data}")

            # Verify environment variables
            if not API_KEY or not APP_ID:
                error_msg = {
                    'error': True,
                    'message': 'Missing API credentials. Please check environment variables.'
                }
                print(f"Error: {error_msg}")
                self._send_response(error_msg, 500)
                return

            # Verify request data
            if not data or 'prompt' not in data:
                error_msg = {
                    'error': True,
                    'message': 'Missing prompt in request'
                }
                print(f"Error: {error_msg}")
                self._send_response(error_msg, 400)
                return

            # Call AI API
            try:
                response = Application.call(
                    api_key=API_KEY,
                    app_id=APP_ID,
                    prompt=data['prompt']
                )
                
                # Print API response for debugging
                print(f"API Response status: {response.status_code}")
                
                if response.status_code != HTTPStatus.OK:
                    error_msg = {
                        'error': True,
                        'message': getattr(response, 'message', 'API call failed'),
                        'request_id': getattr(response, 'request_id', None),
                        'code': response.status_code
                    }
                    print(f"API Error: {error_msg}")
                    self._send_response(error_msg, response.status_code)
                    return

                # Print successful response
                print("Successful API response")
                self._send_response({
                    'output': {
                        'text': response.output.text
                    }
                })

            except Exception as api_error:
                error_msg = {
                    'error': True,
                    'message': f'API call failed: {str(api_error)}'
                }
                print(f"API Error: {error_msg}")
                self._send_response(error_msg, 500)

        except Exception as e:
            error_msg = {
                'error': True,
                'message': f'Server error: {str(e)}'
            }
            print(f"Server Error: {error_msg}")
            self._send_response(error_msg, 500)

    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        response_data = json.dumps(data).encode('utf-8')
        print(f"Sending response: {response_data}")
        self.wfile.write(response_data) 