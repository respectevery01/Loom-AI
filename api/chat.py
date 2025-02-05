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
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Verify environment variables
            if not API_KEY or not APP_ID:
                self._send_response({
                    'error': True,
                    'message': 'Missing API credentials'
                }, 500)
                return

            # Verify request data
            if not data or 'prompt' not in data:
                self._send_response({
                    'error': True,
                    'message': 'Missing prompt in request'
                }, 400)
                return

            # Call AI API
            response = Application.call(
                api_key=API_KEY,
                app_id=APP_ID,
                prompt=data['prompt']
            )

            if response.status_code != HTTPStatus.OK:
                self._send_response({
                    'error': True,
                    'message': response.message,
                    'request_id': response.request_id,
                    'code': response.status_code
                }, response.status_code)
                return

            self._send_response({
                'output': {
                    'text': response.output.text
                }
            })

        except Exception as e:
            self._send_response({
                'error': True,
                'message': str(e)
            }, 500)

    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8')) 