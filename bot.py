import os
import re
import requests
from telebot import TeleBot, types
from instaloader import Instaloader, Post

# ======== تنظیمات ========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN پیدا نشد!")

bot = TeleBot(BOT_TOKEN)

# ======== اطلاعات ورود به اینستاگرام ========
INSTA_USERNAME = "Sedaye_you"
INSTA_PASSWORD = "Q1w2e3r4h."

# ======== دانلودر اینستاگرام ========
def download_instagram(url):
    try:
        L = Instaloader()
        L.login(INSTA_USERNAME, INSTA_PASSWORD)
        L.save_metadata = False
        L.post_metadata_txt_pattern = ""
        
        shortcode = url.split("/p/")[1].split("/")[0]
        post = Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target="temp")
        
        files = os.listdir("temp")
        if files:
            file_path = os.path.join("temp", files[0])
            return file_path, post.is_video
        return None, None
    
    except Exception as e:
        return None, str(e)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎯 لینک اینستاگرام رو بفرست تا برات دانلود کنم.")

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    text = message.text
    pattern = r'(https?://(?:www\.)?instagram\.com/(?:p|reel|tv|stories)/[A-Za-z0-9_-]+)'
    match = re.search(pattern, text)
    
    if not match:
        bot.reply_to(message, "❌ لینک معتبر اینستاگرام نیست!")
        return
    
    url = match.group(1)
    msg = bot.reply_to(message, "⏳ در حال دانلود...")
    
    file_path, is_video = download_instagram(url)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                if is_video:
                    bot.send_video(message.chat.id, f)
                else:
                    bot.send_photo(message.chat.id, f)
            
            os.remove(file_path)
            os.rmdir("temp")
            bot.delete_message(message.chat.id, msg.message_id)
            
        except Exception as e:
            bot.reply_to(message, f"❌ خطا در ارسال: {e}")
    else:
        bot.reply_to(message, f"❌ دانلود ناموفق! خطا: {file_path}")

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    print("🤖 ربات روشن شد...")
    bot.infinity_polling()
