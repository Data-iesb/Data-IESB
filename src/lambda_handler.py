"""
AWS Lambda handler for Amazon Q Business Chatbot
Serverless deployment option
"""

import json
import os
from chatbot_backend import QBusinessChatbot

# Initialize chatbot outside handler for reuse
chatbot = QBusinessChatbot()

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    try:
        # Parse the request
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Handle different endpoints
        if path == '/' and http_method == 'GET':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'Amazon Q Business Chatbot (Lambda)',
                    'configured': bool(chatbot.q_business_client and chatbot.application_id)
                })
            }
        
        elif path == '/chat' and http_method == 'POST':
            # Parse request body
            body = json.loads(event.get('body', '{}'))
            
            if 'message' not in body:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Invalid request',
                        'message': 'Message is required'
                    })
                }
            
            user_message = body['message'].strip()
            conversation_id = body.get('conversationId')
            
            if not user_message:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Empty message',
                        'message': 'Please provide a non-empty message'
                    })
                }
            
            # Get response from Q Business
            response = chatbot.chat_with_q_business(user_message, conversation_id)
            
            status_code = 200 if 'error' not in response else 500
            
            return {
                'statusCode': status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response)
            }
        
        elif http_method == 'OPTIONS':
            # Handle CORS preflight
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': ''
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Not found',
                    'message': f'Path {path} not found'
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
                'error': 'Server error',
                'message': str(e)
            })
        }
