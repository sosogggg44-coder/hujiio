import requests
import json
import sys
import io

# Force UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VIDEO_ID = "6_9ZiuONXt0"
PROXIES = [
    "https://api.allorigins.win/raw?url=",
    "https://corsproxy.io/?",
    "https://api.codetabs.com/v1/proxy?quest="
]

def test_proxies():
    print(f"[*] Testing Proxies for Video: {VIDEO_ID}")
    target = f"https://www.youtube.com/watch?v={VIDEO_ID}"
    
    for p in PROXIES:
        print(f"  > Testing: {p}...")
        try:
            res = requests.get(f"{p}{target}", timeout=10)
            if res.status_code == 200:
                html = res.text
                if '"INNERTUBE_API_KEY"' in html:
                    print(f"    [+] SUCCESS: Found API Key via {p}")
                else:
                    print(f"    [?] Proxy worked but no API Key in HTML (YouTube Blocked?)")
            else:
                print(f"    [!] HTTP {res.status_code}")
        except Exception as e:
            print(f"    [X] Failed: {e}")

if __name__ == "__main__":
    test_proxies()
