import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
target_channel = os.environ.get("TARGET_CHANNEL", "@dealofcheapest")

source_channels = ['deals', 'lootdealsapp']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        text = event.raw_text or ""
        if event.media:
            await client.send_file(target_channel, event.media, caption=text)
        else:
            await client.send_message(target_channel, text)
        print("Deal posted successfully!")
    except Exception as e:
        print(f"Error: {e}")

print("Bot started on Cloud...")
client.start()
client.run_until_disconnected()
