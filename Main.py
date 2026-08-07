import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Dummy web server to keep it FREE
def run_server():
    server_address = ('0.0.0.0', int(os.environ.get("PORT", 10000)))
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Telegram Bot Code
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_channel = os.environ.get("TARGET_CHANNEL", "@dealofcheapest")

source_channels = ['deals', 'lootdealsapp']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        # Get message text, format, and buttons/links
        text = event.text or ""
        formatting = event.entities
        buttons = event.reply_markup

        if event.media:
            await client.send_file(target_channel, event.media, caption=text, formatting_entities=formatting, reply_markup=buttons)
        else:
            await client.send_message(target_channel, text, formatting_entities=formatting, reply_markup=buttons)
        print("Deal with links posted successfully!")
    except Exception as e:
        print(f"Error: {e}")

print("Bot started on Cloud...")
client.start()
client.run_until_disconnected()
