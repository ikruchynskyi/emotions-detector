from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import emotionAnalyzer
import sys

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_length)
        if self.path == '/analyze':
            result = process(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result)
        else:
            self.send_error(404)

def process(data):
    # Do some processing with the post data
    # and return the result as a JSON string
    data = json.loads(data.decode('utf-8'))
    # Extract the text from the JSON object and analyze its emotion
    text = data.get('text', '')
    emotion = emotionAnalyzer.analyze(text)[0]['label']
    result = {'status': 'success', 'data': emotion}
    return json.dumps(result).encode('utf-8')

def run(address, port, server_class=HTTPServer, handler_class=RequestHandler):
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n" + sys.argv[0] + " [address] [port]")
        sys.exit(1)

    run(sys.argv[1], int(sys.argv[2]))

