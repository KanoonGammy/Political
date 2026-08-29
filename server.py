import http.server
import socketserver
import os
import sys
import webbrowser

PORT = 17325
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run(port: int = None):
    if port is None:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    url = f"http://localhost:{port}"
    
    # Allow socket address reuse to prevent 'Address already in use' errors
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"===========================================================")
        print(f" [*] Thai Politics Semantic Graph Dashboard")
        print(f" [*] Running live on: {url}")
        print(f" [*] Serving directory: {DIRECTORY}")
        print(f" [*] Press Ctrl+C to stop the server")
        print(f"===========================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped.")

if __name__ == "__main__":
    run()
