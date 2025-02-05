from http import HTTPStatus
import json
import os
import dashscope
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

def handler(request):
    """
    request - function parameters:
        method: str
        body: str
        query: dict
        cookies: dict
        headers: dict
    """
    # Handle CORS preflight request
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        }

    # Parse request body
    try:
        body = json.loads(request.get('body', '{}'))
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': True,
                'message': f'Invalid request body: {str(e)}'
            })
        }

    # Check API key
    if not DASHSCOPE_API_KEY:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': True,
                'message': 'Missing API credentials'
            })
        }

    # Check prompt
    if not body or 'prompt' not in body:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': True,
                'message': 'Missing prompt in request'
            })
        }

    # Call AI API
    try:
        response = dashscope.Generation.call(
            model='qwen-max',
            api_key=DASHSCOPE_API_KEY,
            prompt=body['prompt']
        )

        if response.status_code != HTTPStatus.OK:
            return {
                'statusCode': response.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': True,
                    'message': getattr(response, 'message', 'API call failed'),
                    'request_id': getattr(response, 'request_id', None),
                    'code': response.status_code
                })
            }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'output': {
                    'text': response.output.text
                }
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': True,
                'message': f'API call failed: {str(e)}'
            })
        } 