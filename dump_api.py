import requests
import re
import json
import sys
import io

# Force UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VIDEO_ID = "6_9ZiuONXt0"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def dump_api():
    print(f"[*] Fetching HTML for {VIDEO_ID}...")
    try:
        session = requests.Session()
        res = session.get(f"https://www.youtube.com/watch?v={VIDEO_ID}", headers={"User-Agent": UA})
        html = res.text
        
        api_key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
        client_ver = re.search(r'"clientVersion":"([^"]+)"', html).group(1)
        visitor_data = re.search(r'"visitorData":"([^"]+)"', html).group(1)
        continuation = re.search(r'"continuation":"([^"]{80,})"', html).group(1)
        
        print(f"  > API Key: {api_key}")
        print(f"  > Continuation: {continuation[:30]}...")
        
        api_url = f"https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key={api_key}"
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": client_ver,
                    "visitorData": visitor_data
                }
            },
            "continuation": continuation
        }
        
        print(f"[*] Posting to InnerTube API...")
        res = session.post(api_url, json=payload, headers={"User-Agent": UA})
        data = res.json()
        
        # Save for analysis
        with open("raw_api_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print("[+] Response saved to raw_api_response.json")
        
        actions = data.get("continuationContents", {}).get("liveChatContinuation", {}).get("actions", [])
        print(f"  > Actions found: {len(actions)}")
        
        if actions:
            print("  > Sample message discovery:")
            for a in actions:
                item = a.get("addChatItemAction", {}).get("item", {}).get("liveChatTextMessageRenderer", {})
                if item:
                    author = item.get("authorName", {}).get("simpleText", "Unknown")
                    msg = "".join([r.get("text", "") for r in item.get("message", {}).get("runs", [])])
                    print(f"    - {author}: {msg}")
                    
    except Exception as e:
        print(f"  [X] API Dump Error: {e}")

if __name__ == "__main__":
    dump_api()
