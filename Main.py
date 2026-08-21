from telethon import TelegramClient, events
import re

# अपनी API ID और Hash यहाँ डालें
api_id = 1234567  
api_hash = 'your_api_hash_here'

# सोर्स चैनल (जहाँ से डील्स उठानी हैं) और अपना चैनल
SOURCE_CHANNELS = ['@source_channel_1', '@source_channel_2']
MY_CHANNEL = '@dealofcheapest'

# यह Set उन सभी लिंक्स को याद रखेगा जो आज पोस्ट हो चुके हैं
posted_deals = set()

client = TelegramClient('deal_bot', api_id, api_hash)

# लिंक्स ढूंढने के लिए Regex (ताकि मैसेज से लिंक निकाला जा सके)
url_pattern = re.compile(r'(https?://[^\s]+)')

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handle_new_deal(event):
    message_text = event.message.text
    
    if message_text:
        # मैसेज में से सभी लिंक्स ढूँढो
        urls = url_pattern.findall(message_text)
        
        # अगर मैसेज में कोई लिंक है
        if urls:
            # हम मुख्य लिंक (आमतौर पर पहला लिंक) चेक करेंगे
            main_url = urls[0] 
            
            # 🛑 डुप्लीकेट चेक: क्या यह लिंक पहले भेजा जा चुका है?
            if main_url in posted_deals:
                print(f"Skipped Duplicate Deal: {main_url}")
                return # अगर डुप्लीकेट है, तो यहीं रुक जाओ और कुछ मत करो
            
            # ✅ अगर नया लिंक है, तो अपने चैनल पर भेजो
            try:
                # यहाँ तुम अपना एफिलिएट लिंक बदलने वाला कोड भी लगा सकते हो
                await client.send_message(MY_CHANNEL, message_text)
                
                # भेजने के बाद इस लिंक को मेमोरी (Set) में सेव कर लो
                posted_deals.add(main_url)
                print(f"Success! New Deal Posted: {main_url}")
                
            except Exception as e:
                print(f"Error posting deal: {e}")

print("Bot is running and listening for fresh deals...")
client.start()
client.run_until_disconnected()
