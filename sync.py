import requests
import re
import json
import sys
import io
import time

# Force UTF-8 for Windows Terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VIDEO_ID = "6_9ZiuONXt0"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def start_engine():
    print(f"[*] VRTICS Sync Engine V7.3 — ID: {VIDEO_ID}")
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    
    # 1. Discovery
    try:
        res = session.get(f"https://www.youtube.com/watch?v={VIDEO_ID}")
        html = res.text
        
        api_key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
        client_ver = re.search(r'"clientVersion":"([^"]+)"', html).group(1)
        visitor_data = re.search(r'"visitorData":"([^"]+)"', html).group(1)
        continuation = re.search(r'"continuation":"([^"]{80,})"', html).group(1)
        
        print(f"[+] Connected. Version: {client_ver}")
        
    except Exception as e:
        print(f"[!] Discovery Failed: {e}")
        return

    # 2. Sync Loop
    seen_ids = set()
    next_cont = continuation
    
    while True:
        try:
            api_url = f"https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key={api_key}"
            payload = {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": client_ver,
                        "visitorData": visitor_data
                    }
                },
                "continuation": next_cont
            }
            
            res = session.post(api_url, json=payload)
            data = res.json()
            
            cont_contents = data.get("continuationContents", {}).get("liveChatContinuation", {})
            
            # Update continuation
            c_data = cont_contents.get("continuations", [{}])[0]
            next_cont = (c_data.get("invalidationContinuationData", {}).get("continuation") or 
                        c_data.get("timedContinuationData", {}).get("continuation") or 
                        c_data.get("reloadContinuationData", {}).get("continuation") or 
                        next_cont)
            
            timeout = c_data.get("timedContinuationData", {}).get("timeoutMs", 2000) / 1000
            
            # Process messages
            actions = cont_contents.get("actions", [])
            for action in actions:
                item = action.get("addChatItemAction", {}).get("item", {}).get("liveChatTextMessageRenderer", {})
                if item:
                    msg_id = item.get("id")
                    if msg_id not in seen_ids:
                        seen_ids.add(msg_id)
                        author = item.get("authorName", {}).get("simpleText", "User")
                        msg = "".join([r.get("text", "") for r in item.get("message", {}).get("runs", [])])
                        print(f"{author}: {msg}")
                        sys.stdout.flush()
            
            # Adaptive sleep
            time.sleep(max(1, timeout))
            
        except Exception as e:
            print(f"[!] Loop Error: {e}")
            time.sleep(5)
            # Re-discover if needed
            session = requests.Session()
            session.headers.update({"User-Agent": UA})

if __name__ == "__main__":
    start_engine()
