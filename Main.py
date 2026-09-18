from telethon import TelegramClient, events
import re
import os

# Screenshot se mili aapki asli API ID aur Hash
api_id = 27889998
api_hash = "f4e43245742ae23336ed35374be88bc8"

# Yahan apne source channels ke username daalein jahan se deals aayengi
SOURCE_CHANNELS = ['@source_channel_1', '@source_channel_2'] 
MY_CHANNEL = "@Dealofcheapest"

posted_deals = set()

client = TelegramClient('deal_bot', api_id, api_hash)

url_pattern = re.compile(r'(https?://[^\s]+)')

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handle_new_deal(event):
    message_text = event.message.text
    
    if message_text:
        urls = url_pattern.findall(message_text)
        
        if urls:
            main_url = urls[0]
            
            if main_url in posted_deals:
                print(f"Skipped Duplicate Deal: {main_url}")
                return
                
            try:
                await client.send_message(MY_CHANNEL, message_text)
                posted_deals.add(main_url)
                print(f"Success: New Deal Posted: {main_url}")
            except Exception as e:
                print(f"Error posting deal: {e}")

print("Bot is running and listening for fresh deals...")

# Yahan aapka MyDealconvertbot ka token daal diya hai
my_bot_token = "8532726197:AAFK_LU8ZtyU5EtwwzctUZxFWzCPkV1232k"
client.start(bot_token=my_bot_token)
client.run_until_disconnected()
