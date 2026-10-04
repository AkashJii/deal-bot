import os
import threading
import re
import urllib.request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# CONFIGURATION (API KEYS & TAGS)
# ==========================================
CUELINKS_API_KEY = "F3x7T2PVXTHKCTJ22CRcqhNqR15cfb8sB9nVwWU="
YOUR_AMAZON_TAG = "dealofcheapes-21"

# ==========================================
# UPTIMEROBOT 24/7 SERVER LOGIC
# ==========================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is ALIVE!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"Web server running on port {port} for UptimeRobot...")
    httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# ==========================================
# TELEGRAM BOT LOGIC
# ==========================================
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_channel = os.environ.get("TARGET_CHANNEL", "@dealofcheapest")

source_channels = ['deals', 'lootdealsapp', 'amazinglootsdealsoffers']
client = TelegramClient(StringSession(session_string), api_id, api_hash)

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
    text = event.text or ""
    
    # URL nikalne ka logic
    urls = re.findall(r'(https?://[^\s]+)', text)
    if not urls:
        return
        
    new_text = text
    for url in urls:
        final_url = url
        # Agar Amazon ka link hai, toh manually tag replace karo
        if "amazon.in" in url or "amazon.com" in url:
            if "tag=" in final_url:
                final_url = re.sub(r'tag=[a-zA-Z0-9_-]+', f'tag={YOUR_AMAZON_TAG}', final_url)
            else:
                separator = "&" if "?" in final_url else "?"
                final_url = f"{final_url}{separator}tag={YOUR_AMAZON_TAG}"
        else:
            # Baaki links ke liye Cuelinks API use karo
            final_url = get_cuelinks_affiliate_url(url)
            
        new_text = new_text.replace(url, final_url)
        
    # Nayi deal aapke channel par bhejna
    try:
        if event.media:
            await client.send_message(target_channel, new_text, file=event.media)
        else:
            await client.send_message(target_channel, new_text)
    except Exception as e:
        print(f"Message send karne mein error: {e}")

print("Bot is starting...")
client.start()
client.run_until_disconnected()
