"""Serves the UI and runs the untouched lost_and_found.py for every found/lost pair.
Usage:  python server.py   then open http://localhost:8000
No extra packages needed (standard library only)."""
import json, os, secrets, subprocess, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(BASE, "lost_and_found.py")
USER, PASS = "admin", "lostfound123"
TOKENS = set()
FILES = {"/": ("index.html", "text/html"), "/index.html": ("index.html", "text/html"),
         "/style.css": ("style.css", "text/css"), "/script.js": ("script.js", "text/javascript")}
KEYS = {"Item", "Color", "Finder", "Finder Phone", "Found Location",
        "Owner", "Owner Phone", "Lost Location"}


def clean(v):
    return " ".join(str(v).splitlines()).strip()[:100]


def run_pair(f, l):
    """Feed one found + one lost item to lost_and_found.py via stdin, parse its printed result."""
    lines = [f["item"], f["color"], f["location"], f["who"], f["phone"],
             l["item"], l["color"], l["location"], l["who"], l["phone"]]
    stdin = "\n".join(clean(x) for x in lines) + "\n"
    r = subprocess.run([sys.executable, SCRIPT], input=stdin,
                       capture_output=True, text=True, timeout=10)
    out = r.stdout.split("--- Matching Results ---")[-1]
    if "Matching Item Found!" not in out:
        return None
    d = {}
    for line in out.splitlines():
        k, _, v = line.partition(":")
        if k in KEYS:
            d[k] = v.strip()
    return d


class H(BaseHTTPRequestHandler):
    def send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        name = FILES.get(self.path.split("?")[0])
        if not name:
            return self.send(404, {"error": "not found"})
        with open(os.path.join(BASE, name[0]), "rb") as fh:
            self.send(200, fh.read(), name[1])

    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except ValueError:
            return self.send(400, {"error": "bad json"})
        if self.path == "/api/login":
            if data.get("username") == USER and data.get("password") == PASS:
                t = secrets.token_hex(16)
                TOKENS.add(t)
                return self.send(200, {"token": t})
            return self.send(401, {"error": "Wrong username or password."})
        if self.path == "/api/match":
            if self.headers.get("X-Token") not in TOKENS:
                return self.send(401, {"error": "login required"})
            found, lost = data.get("found", [])[:30], data.get("lost", [])[:30]
            matches = [m for f in found for l in lost if (m := run_pair(f, l))]
            return self.send(200, {"matches": matches})
        self.send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("Lost & Found running at http://localhost:8000  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", 8000), H).serve_forever()
