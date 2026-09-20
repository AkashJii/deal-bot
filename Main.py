import os
import threading
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# 🚀 CONFIGURATION
# ==========================================
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

# Naya channel 'amazinglootsdealsoffers' add kar diya hai
source_channels = ['deals', 'lootdealsapp', 'amazinglootsdealsoffers']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        text = event.text or ""
        text_lower = text.lower()
        
        # 1. Amazon Filter: Sirf Amazon deals ko aage badhne dega
        if "amazon" not in text_lower and "amzn" not in text_lower:
            return

        # 2. Amazon Tag Magic 🪄
        # Purane tag ko aapke tag me badal dega
        text = re.sub(r'tag=[a-zA-Z0-9_-]+', f'tag={YOUR_AMAZON_TAG}', text)
        
        # Agar kisi link me tag nahi hai, to add kar dega
        urls = re.findall(r'(https?://[^\s]+)', text)
        for url in urls:
            if "amazon.in" in url.lower() and "tag=" not in url.lower():
                separator = "&" if "?" in url else "?"
                new_url = f"{url}{separator}tag={YOUR_AMAZON_TAG}"
                text = text.replace(url, new_url)

        # 3. Post to Channel 🚀
        if event.media:
            await client.send_file(target_channel, event.media, caption=text)
        else:
            await client.send_message(target_channel, text)
            
        print("Amazon Deal successfully posted with your Tag!")
    except Exception as e:
        print(f"Error in processing deal: {e}")

print("Bot started... Listening ONLY for Amazon Loots!")
client.start()
client.run_until_disconnected()
