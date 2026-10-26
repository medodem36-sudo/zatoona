# -*- coding: utf-8 -*-
import urllib.request
import ssl

url = "https://services.gradle.org/distributions/gradle-8.5-bin.zip"
print(f"Checking {url}...")
try:
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"Status: {resp.status}")
        print(f"Content-Length: {resp.headers.get('Content-Length')} bytes")
except Exception as e:
    print(f"Error: {e}")
