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
            
            query = data.get('query', '').strip()
            
            if not query:
                self.wfile.write(json.dumps({'error': 'Query is required'}).encode())
                return
            
            # Test just the imports first
            try:
                import requests
                import_status = "requests: OK"
            except Exception as e:
                import_status = f"requests: FAILED - {e}"
                
            try:
                import psycopg2
                import_status += ", psycopg2: OK"
            except Exception as e:
                import_status += f", psycopg2: FAILED - {e}"
            
            # Simple response without complex operations
            response = {
                'query': query,
                'message': 'Simplified endpoint working',
                'imports': import_status,
                'env_check': {
                    'hf_token': os.getenv('HUGGINGFACE_API_TOKEN')[:10] + '...' if os.getenv('HUGGINGFACE_API_TOKEN') else 'Missing',
                    'gemini_key': os.getenv('GEMINI_API_KEY')[:10] + '...' if os.getenv('GEMINI_API_KEY') else 'Missing',
                    'db_url': 'postgresql://...' if os.getenv('NEON_DATABASE_URL') else 'Missing'
                },
                'status': 'success'
            }
            
        except Exception as e:
            response = {
                'error': f'Error: {str(e)}',
                'status': 'failed'
            }
            
        self.wfile.write(json.dumps(response, indent=2).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
