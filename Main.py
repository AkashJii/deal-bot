import os
import threading
import re
import urllib.request
import urllib.parse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# 🚀 CO-FOUNDER CONFIGURATION (API KEYS)
# ==========================================
CUELINKS_API_KEY = "F3x7T2PXVTKHcTj22CRcqhNqR15cfb8sB9nVuwJRPuM"
YOUR_AMAZON_TAG = "dealofcheapes-21"

# ==========================================
# 🟢 UPTIMEROBOT 24/7 SERVER LOGIC
# ==========================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# ==========================================
# 🤖 TELEGRAM BOT LOGIC
# ==========================================
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_channel = os.environ.get("TARGET_CHANNEL", "@dealofcheapest")
source_channels = ['deals', 'lootdealsapp']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Cuelinks API Function
def get_cuelinks_affiliate_url(original_url):
    try:
        api_endpoint = "https://api.cuelinks.com/v3/links/generate"
        headers = {
            "Authorization": f"Bearer {CUELINKS_API_KEY}",
            "Content-Type": "application/json"
        }
        data = json.dumps({"url": original_url}).encode("utf-8")
        
        req = urllib.request.Request(api_endpoint, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode())
            return res_data.get("url", original_url) 
    except Exception as e:
        print(f"Cuelinks Warning: {e}")
        return original_url

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        text = event.text or ""
        
        # 0. Quality & Spam Filter (कचरा डील्स को बाहर निकालने के लिए)
        text_lower = text.lower()
        if len(text.strip()) < 15:
            return
        if "rs." not in text_lower and "₹" not in text_lower and "off" not in text_lower:
            return

        # 1. Amazon Tag Magic 🪄
        text = re.sub(r'tag=[a-zA-Z0-9_-]+', f'tag={YOUR_AMAZON_TAG}', text)
        
        # 2. Flipkart / Shopsy Link Cleaning & Cuelinks Magic 🪄
        urls = re.findall(r'(https?://[^\s]+)', text)
        for url in urls:
            if "amazon" not in url.lower() and "amzn" not in url.lower():
                base_url = url.split('&affid=')[0].split('?affid=')[0].split('&src=')[0].split('?src=')[0]
                
                affiliated_url = get_cuelinks_affiliate_url(base_url)
                if affiliated_url != base_url:
                    text = text.replace(url, affiliated_url)
        
        # 3. Post to Channel 🚀
        if event.media:
            await client.send_file(target_channel, event.media, caption=text)
        else:
            await client.send_message(target_channel, text)
            
        print("Filtered & Cleaned Deal successfully posted!")
    except Exception as e:
        print(f"Error in processing deal: {e}")

print("Bot started on Cloud with Smart Filters...")
client.start()
client.run_until_disconnected()
