import os
import threading
import re
import urllib.request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# 🚀 CONFIGURATION (API KEYS & TAGS)
# ==========================================
CUELINKS_API_KEY = "F3x7T2PXVTKHcTj22CRcqhNqR15cfb8sB9nVuwJRPuM"
YOUR_AMAZON_TAG = "dealofcheapes-21"

# ==========================================
# 🟢 UPTIMEROBOT 24/7 SERVER LOGIC (FIXED)
# ==========================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # UptimeRobot ko clear signal bhejega ki bot zinda hai
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is ALIVE!")
        
    def log_message(self, format, *args):
        pass # Terminal ko clean rakhne ke liye server logs hide kiye hain

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"Web server running on port {port} for UptimeRobot...")
    httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# ==========================================
# 🤖 TELEGRAM BOT LOGIC
# ==========================================
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_channel = os.environ.get("TARGET_CHANNEL", "@dealofcheapest")

# Yahan teeno source channels added hain
source_channels = ['deals', 'lootdealsapp', 'amazinglootsdealsoffers']

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
        return original_url

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        text = event.text or ""
        if not text.strip():
            return
        
        # 1. Amazon Tag Update (Agar purana tag laga hai toh usko replace karega)
        text = re.sub(r'tag=[a-zA-Z0-9_-]+', f'tag={YOUR_AMAZON_TAG}', text)
        
        # 2. Saare URLs dhundo aur unhe convert karo
        urls = re.findall(r'(https?://[^\s]+)', text)
        for url in urls:
            if "amazon" in url.lower() or "amzn" in url.lower():
                # Agar Amazon link me tag nahi hai, toh add karega
                if "tag=" not in url.lower():
                    separator = "&" if "?" in url else "?"
                    new_url = f"{url}{separator}tag={YOUR_AMAZON_TAG}"
                    text = text.replace(url, new_url)
            else:
                # Non-Amazon (Flipkart/Myntra/etc) deals ko Cuelinks ke through bhejega
                base_url = url.split('&affid=')[0].split('?affid=')[0].split('&src=')[0].split('?src=')[0]
                affiliated_url = get_cuelinks_affiliate_url(base_url)
                if affiliated_url != base_url:
                    text = text.replace(url, affiliated_url)

        # 3. Deal of Cheapest me forward karna
        if event.media:
            await client.send_file(target_channel, event.media, caption=text)
        else:
            await client.send_message(target_channel, text)
            
        print("Success: Deal Processed & Posted!")
    except Exception as e:
        print(f"Error in processing deal: {e}")

print("Bot started... Listening for ALL Deals!")
client.start()
client.run_until_disconnected()
