import http.server, socketserver, os, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
DIRECTORY = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "deploy")

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIRECTORY, **k)

class S(socketserver.TCPServer):
    allow_reuse_address = True

with S(("", PORT), H) as httpd:
    print("serving %s on %d" % (DIRECTORY, PORT))
    httpd.serve_forever()
