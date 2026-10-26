"""
cdp_client.py
Minimal standard-library WebSocket client for Chrome DevTools Protocol (CDP).
Enables zero-dependency JavaScript evaluation in Android WebViews.
"""
import sys
import socket
import base64
import os
import json
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def get_ws_url():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    targets = json.loads(req.read().decode())
    for t in targets:
        if t.get('type') == 'page':
            return t.get('webSocketDebuggerUrl')
    return None


class SimpleWebSocket:
    def __init__(self, ws_url):
        # ws://127.0.0.1:9222/devtools/page/...
        clean_url = ws_url.replace('ws://', '')
        host_port, path = clean_url.split('/', 1)
        host, port = host_port.split(':')
        self.path = '/' + path

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, int(port)))

        # Handshake
        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        handshake = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode('utf-8'))

        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)

    def send_text(self, text):
        data = text.encode('utf-8')
        length = len(data)
        frame = bytearray([0x81])  # FIN + Text frame
        mask = os.urandom(4)

        if length <= 125:
            frame.append(0x80 | length)
        elif length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(length.to_bytes(2, 'big'))
        else:
            frame.append(0x80 | 127)
            frame.extend(length.to_bytes(8, 'big'))

        frame.extend(mask)
        masked_data = bytearray(b ^ mask[i % 4] for i, b in enumerate(data))
        frame.extend(masked_data)
        self.sock.sendall(frame)

    def recv_text(self):
        # Read header
        header = self.sock.recv(2)
        if len(header) < 2:
            return None
        length = header[1] & 0x7F
        if length == 126:
            length = int.from_bytes(self.sock.recv(2), 'big')
        elif length == 127:
            length = int.from_bytes(self.sock.recv(8), 'big')

        payload = b""
        while len(payload) < length:
            payload += self.sock.recv(length - len(payload))
        return payload.decode('utf-8', errors='replace')

    def close(self):
        try:
            self.sock.close()
        except:
            pass


def eval_js(js_expr):
    ws_url = get_ws_url()
    if not ws_url:
        return {"error": "No page target found"}

    ws = SimpleWebSocket(ws_url)
    req = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_expr,
            "returnByValue": True,
            "awaitPromise": True
        }
    }
    ws.send_text(json.dumps(req))

    while True:
        msg = ws.recv_text()
        if not msg:
            break
        data = json.loads(msg)
        if data.get("id") == 1:
            ws.close()
            return data.get("result", {}).get("result", {}).get("value")
    ws.close()
    return None


if __name__ == '__main__':
    expr = sys.argv[1] if len(sys.argv) > 1 else "location.href"
    res = eval_js(expr)
    print(json.dumps(res, ensure_ascii=False, indent=2))
