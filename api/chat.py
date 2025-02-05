from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json
import os
import dashscope
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_APP_ID = os.getenv('DASHSCOPE_APP_ID', '55b67db129d340749cfce41cbc162ed7')

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            # Read request body
            request_body = self.rfile.read(content_length)
            # Parse JSON
            body = json.loads(request_body.decode('utf-8'))

            # Check API key
            if not DASHSCOPE_API_KEY:
                self._send_error_response(500, 'Missing API credentials')
                return

            # Check prompt
            if not body or 'prompt' not in body:
                self._send_error_response(400, 'Missing prompt in request')
                return

            # Call AI API
            try:
                response = dashscope.Application.call(
                    api_key=DASHSCOPE_API_KEY,
                    app_id=DASHSCOPE_APP_ID,
                    prompt=body['prompt']
                )

                if response.status_code != HTTPStatus.OK:
                    error_msg = {
                        'error': True,
                        'message': getattr(response, 'message', 'API call failed'),
                        'request_id': getattr(response, 'request_id', None),
                        'code': response.status_code
                    }
                    self._send_error_response(response.status_code, error_msg)
                    return

                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_body = json.dumps({
                    'output': {
                        'text': response.output.text
                    }
                })
                self.wfile.write(response_body.encode('utf-8'))

            except Exception as e:
                self._send_error_response(500, f'API call failed: {str(e)}')

        except Exception as e:
            self._send_error_response(500, f'Server error: {str(e)}')

    def _send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_body = json.dumps({
            'error': True,
            'message': message
        })
        self.wfile.write(error_body.encode('utf-8')) 