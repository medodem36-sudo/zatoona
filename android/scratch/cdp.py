import socket
import json
import urllib.request
import os
import re

def get_ws_url():
    data = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
    return data[0]["webSocketDebuggerUrl"]

def cdp_eval(expr):
    ws_url = get_ws_url()
    path = ws_url.split("localhost:9222")[1]

    s = socket.socket()
    s.connect(("localhost", 9222))

    key = "dGhlIHNhbXBsZSBub25jZQ=="
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:9222\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode())

    resp = s.recv(4096)
    assert b"101 " in resp, f"Handshake failed: {resp}"

    msg = json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": True
        }
    }).encode("utf-8")

    mask = os.urandom(4)
    length = len(msg)

    if length < 126:
        header = bytes([0x81, 0x80 | length]) + mask
    elif length < 65536:
        header = bytes([0x81, 0x80 | 126]) + length.to_bytes(2, "big") + mask
    else:
        header = bytes([0x81, 0x80 | 127]) + length.to_bytes(8, "big") + mask

    masked = bytearray(msg)
    for i in range(len(masked)):
        masked[i] ^= mask[i % 4]

    s.sendall(header + masked)

    # Read response
    data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if b"\"id\":1" in data and b"\"result\"" in data:
            break

    s.close()

    # In websocket frame, payload starts after 2 bytes (unmasked from server)
    # Let's decode UTF-8 with ignore and find JSON
    text = data.decode("utf-8", errors="ignore")
    m = re.search(r'\{.*"id":1.*\}', text)
    if m:
        return json.loads(m.group(0))
    return text

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    res = cdp_eval("document.title")
    print("CDP Result:", res.get("result", {}).get("result", {}).get("value"))
