import http.server
import socketserver

PORT = 5000
HOST = "0.0.0.0"

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

with socketserver.TCPServer((HOST, PORT), NoCacheHandler) as httpd:
    print(f"Serving at http://{HOST}:{PORT}")
    httpd.serve_forever()
