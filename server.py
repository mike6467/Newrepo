import http.server
import socketserver
import os
from urllib.parse import unquote

PORT = 5000
HOST = "0.0.0.0"

# Map clean paths to their actual HTML files (mirrors _redirects)
REDIRECTS = {
    "/wallet": "/wallet.html",
}

# Block access to hidden paths and sensitive files
BLOCKED_PREFIXES = (".", "_")
BLOCKED_NAMES = {".git", ".replit", ".cache", ".agents", ".local", "_redirects"}


class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self._handle()

    def do_HEAD(self):
        self._handle()

    def _handle(self):
        raw_path = self.path.split("?")[0]

        # Decode percent-encoding repeatedly until stable (guards against double-encoding)
        decoded = raw_path
        while True:
            next_decoded = unquote(decoded)
            if next_decoded == decoded:
                break
            decoded = next_decoded

        path = decoded.rstrip("/") or "/"

        # Block hidden/sensitive paths (checked on fully-decoded segments)
        parts = [p for p in path.split("/") if p]
        if any(p.startswith(".") or p in BLOCKED_NAMES for p in parts):
            self.send_error(403, "Forbidden")
            return

        # Apply clean-URL redirects
        if path in REDIRECTS:
            self.path = REDIRECTS[path]
            super().do_GET() if self.command == "GET" else super().do_HEAD()
            return

        super().do_GET() if self.command == "GET" else super().do_HEAD()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress default per-request logging noise
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


with ReusableTCPServer((HOST, PORT), SecureHandler) as httpd:
    print(f"Serving at http://{HOST}:{PORT}")
    httpd.serve_forever()
