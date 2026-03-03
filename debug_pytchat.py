import pytchat
import time
import sys

video_id = "6_9ZiuONXt0"

def debug_pytchat():
    print(f"[*] Testing Pytchat for ID: {video_id}")
    try:
        chat = pytchat.create(video_id=video_id)
        if chat.is_alive():
            print("[+] Pytchat is ALIVE. Waiting for messages (10s)...")
            start = time.time()
            while chat.is_alive() and time.time() - start < 15:
                items = chat.get().items
                if items:
                    print(f"[!] RECEIVED {len(items)} MESSAGES!")
                    for c in items:
                        print(f"  > {c.author.name}: {c.message}")
                    return True
                time.sleep(1)
            print("[?] No messages received in 15s. Is the chat active?")
        else:
            print("[!] Pytchat could not connect (Not Alive).")
    except Exception as e:
        print(f"[X] Pytchat CRASHED: {e}")
    return False

if __name__ == "__main__":
    debug_pytchat()
