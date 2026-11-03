import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

POD_NAME = os.environ.get("POD_NAME", "unknown")
POD_IP = os.environ.get("POD_IP", "unknown")
UNREADY_FLAG = "/tmp/unready"

ITEMS = [
    {"sku": "A100", "name": "Keyboard", "qty": 42},
    {"sku": "B200", "name": "Mouse", "qty": 17},
    {"sku": "C300", "name": "Monitor", "qty": 8},
]


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/ready":
            if os.path.exists(UNREADY_FLAG):
                self._send(503, {"ready": False, "pod": POD_NAME})
            else:
                self._send(200, {"ready": True, "pod": POD_NAME})
        elif self.path == "/items":
            self._send(200, {"pod": POD_NAME, "podIP": POD_IP, "items": ITEMS})
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        if self.path != "/ready":
            print(f"[{POD_NAME}] {self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"Inventory service starting on :8080 as {POD_NAME} ({POD_IP})", flush=True)
    ThreadingHTTPServer(("", 8080), Handler).serve_forever()
