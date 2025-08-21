from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Test environment variables
            env_status = {
                'HUGGINGFACE_API_TOKEN': 'SET' if os.getenv('HUGGINGFACE_API_TOKEN') else 'MISSING',
                'GEMINI_API_KEY': 'SET' if os.getenv('GEMINI_API_KEY') else 'MISSING', 
                'NEON_DATABASE_URL': 'SET' if os.getenv('NEON_DATABASE_URL') else 'MISSING'
            }
            
            response = {
                'message': 'Debug endpoint working',
                'query_received': data.get('query', 'No query'),
                'environment': env_status,
                'status': 'ok'
            }
            
        except Exception as e:
            response = {
                'error': str(e),
                'status': 'error'
            }
            
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_GET(self):
        self.do_POST()
