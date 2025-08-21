from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.parse

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
            
            # Test embedding using urllib (built-in)
            embedding = self.get_embedding_urllib(query)
            
            if embedding:
                response = {
                    'query': query,
                    'embedding_dimensions': len(embedding),
                    'message': 'Embedding generated successfully using built-in urllib!',
                    'model': 'BAAI/bge-small-en-v1.5',
                    'status': 'success'
                }
            else:
                response = {
                    'query': query,
                    'error': 'Failed to generate embedding',
                    'status': 'failed'
                }
            
        except Exception as e:
            response = {
                'error': f'Error: {str(e)}',
                'status': 'failed'
            }
            
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def get_embedding_urllib(self, text):
        """Generate embedding using urllib instead of requests"""
        try:
            url = 'https://api-inference.huggingface.co/models/BAAI/bge-small-en-v1.5'
            
            # Prepare data
            data = json.dumps({'inputs': text}).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(url, data=data)
            req.add_header('Authorization', f'Bearer {os.getenv("HUGGINGFACE_API_TOKEN")}')
            req.add_header('Content-Type', 'application/json')
            
            # Make request
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    if isinstance(result, list) and len(result) == 384:
                        return result
                    else:
                        return None
                else:
                    return None
                    
        except Exception as e:
            print(f"Embedding error: {e}")
            return None
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
