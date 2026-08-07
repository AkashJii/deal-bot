import os
import threading
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# UptimeRobot को 'All Okay' बोलने वाला सर्वर
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

# Telegram Bot Code
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_channel = os.environ.get("TARGET_CHANNEL", "@dealofcheapest")

source_channels = ['deals', 'lootdealsapp']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# आपका अपना Amazon Affiliate Tag
YOUR_AMAZON_TAG = "dealofcheapes-21"

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        # 1. मैसेज का टेक्स्ट उठाओ
        text = event.text or ""
        
        # 2. जादू (Magic): किसी भी पुराने Amazon टैग को अपने टैग से बदल दो
        modified_text = re.sub(r'tag=[a-zA-Z0-9_-]+', f'tag={YOUR_AMAZON_TAG}', text)
        
        # 3. मैसेज को आपके चैनल पर भेज दो 
        if event.media:
            await client.send_file(target_channel, event.media, caption=modified_text)
        else:
            await client.send_message(target_channel, modified_text)
            
        print("Deal posted with YOUR Amazon tag!")
    except Exception as e:
        print(f"Error: {e}")

print("Bot started on Cloud...")
client.start()
client.run_until_disconnected()
