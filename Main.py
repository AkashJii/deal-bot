import telebot
import os
import re

# Render se direct apka token uthayega
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8532726197:AAFK_LU8ZtyU5EtwwzctUZxFWzCPkV1232k")
bot = telebot.TeleBot(BOT_TOKEN)

MY_CHANNEL = "@Dealofcheapest"
posted_deals = set()

# Links dhundhne ka formula
url_pattern = re.compile(r'(https?://[^\s]+)')

# Ye bot ko aane wale har message ko read karne me help karega
@bot.message_handler(func=lambda message: True, content_types=['text'])
@bot.channel_post_handler(func=lambda message: True, content_types=['text'])
def handle_new_deal(message):
    message_text = message.text
    if not message_text:
        return
        
    urls = url_pattern.findall(message_text)
    
    if urls:
        main_url = urls[0]
        
        # Check karna ki deal pehle toh nahi daali
        if main_url in posted_deals:
            print(f"Skipped Duplicate Deal: {main_url}")
            return
            
        try:
            # Deal of Cheapest channel me forward karna
            bot.send_message(MY_CHANNEL, message_text)
            posted_deals.add(main_url)
            print(f"Success: New Deal Posted: {main_url}")
        except Exception as e:
            print(f"Error posting deal: {e}")

print("Bot is running and listening for fresh deals without API ID/Hash...")
bot.infinity_polling()
