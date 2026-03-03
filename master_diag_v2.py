import pytchat
import requests
import re
import sys
import io
import time

# Force UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_VIDEO_ID = "6_9ZiuONXt0"
BUSY_VIDEO_ID = "9pI12v7c8v4" # Example: BBC News or similar high-activity live

def check_video(vid_id, name):
    print(f"\n[{name}] Checking ID: {vid_id}...")
    url = f"https://www.youtube.com/watch?v={vid_id}"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        html = res.text
        
        is_live = '"isLive":true' in html
        chat_found = 'liveChatRenderer' in html
        sub_only = 'isSubscribersOnly":true' in html
        
        print(f"  > Live: {is_live}")
        print(f"  > Chat Component: {chat_found}")
        print(f"  > Subscribers Only: {sub_only}")
        
        if not is_live or not chat_found:
            print("  [!] FAIL: No active live chat found.")
            return False
            
        print("  > Connecting Pytchat...")
        chat = pytchat.create(video_id=vid_id)
        start_time = time.time()
        while chat.is_alive() and time.time() - start_time < 15:
            items = chat.get().items
            if items:
                print(f"  [!!!] SUCCESS: Received {len(items)} messages!")
                for c in items[:2]:
                    print(f"    - {c.author.name}: {c.message}")
                return True
            time.sleep(1)
        print("  > No messages received after 15s.")
    except Exception as e:
        print(f"  [X] Error: {e}")
    return False

if __name__ == "__main__":
    check_video(USER_VIDEO_ID, "USER_STREAM")
    # check_video(BUSY_VIDEO_ID, "CONTROL_STREAM")
