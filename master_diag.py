import pytchat
import requests
import re
import sys
import io

# Force UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VIDEO_ID = "6_9ZiuONXt0"
URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"

def check_raw_html():
    print("[1] Checking Raw YouTube HTML...")
    try:
        res = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        html = res.text
        
        api_key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
        is_live = '"isLive":true' in html
        chat_found = 'liveChatRenderer' in html
        
        print(f"  > Live: {is_live}")
        print(f"  > API Key: {api_key.group(1) if api_key else 'NOT FOUND'}")
        print(f"  > Chat Component: {chat_found}")
        
        if not is_live:
            print("  [!] WARNING: Video does not report as LIVE.")
            
        cont = re.search(r'"continuation":"([^"]{80,})"', html)
        print(f"  > Continuation: {'FOUND' if cont else 'NOT FOUND'}")
        
        return html
    except Exception as e:
        print(f"  [X] HTML Fetch Error: {e}")
    return None

def test_pytchat():
    print("\n[2] Testing Pytchat Library...")
    try:
        chat = pytchat.create(video_id=VIDEO_ID)
        if chat.is_alive():
            print("  > Pytchat connected. Monitoring for 10s...")
            for _ in range(10):
                if not chat.is_alive(): break
                items = chat.get().items
                if items:
                    print(f"  [!] SUCCESS: Received {len(items)} messages!")
                    for c in items:
                        print(f"    - {c.author.name}: {c.message}")
                    return True
                import time
                time.sleep(1)
            print("  > No messages received in 10s.")
        else:
            print("  > Pytchat failed to stay alive.")
    except Exception as e:
        print(f"  [X] Pytchat Error: {e}")
    return False

if __name__ == "__main__":
    check_raw_html()
    test_pytchat()
