import os
import re
import requests
from telebot import TeleBot, types
from instaloader import Instaloader, Post

# ======== تنظیمات ========
BOT_TOKEN = "8808018168:AAE100BK0sM--JUeE4oPJo5NlDgxWgp2l_Q"  # از @BotFather بگیر
bot = TeleBot(BOT_TOKEN)

# ======== دانلودر اینستاگرام ========
def download_instagram(url):
    try:
        L = Instaloader()
        # فقط دانلود کن، هیچ چیز اضافی ذخیره نکن
        L.save_metadata = False
        L.post_metadata_txt_pattern = ""
        
        # دریافت پست
        post = Post.from_shortcode(L.context, url.split("/p/")[1].split("/")[0])
        
        # دانلود
        L.download_post(post, target="temp")
        
        # پیدا کردن فایل دانلود شده
        files = os.listdir("temp")
        if files:
            file_path = os.path.join("temp", files[0])
            return file_path, post.is_video
        return None, None
    
    except Exception as e:
        return None, str(e)

# ======== دستور استارت ========
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎯 لینک اینستاگرام رو بفرست تا برات دانلود کنم.")

# ======== دریافت لینک ========
@bot.message_handler(func=lambda m: True)
def handle_link(message):
    text = message.text
    
    # چک کردن لینک اینستاگرام
    pattern = r'(https?://(?:www\.)?instagram\.com/(?:p|reel|tv|stories)/[A-Za-z0-9_-]+)'
    match = re.search(pattern, text)
    
    if not match:
        bot.reply_to(message, "❌ لینک معتبر اینستاگرام نیست!")
        return
    
    url = match.group(1)
    msg = bot.reply_to(message, "⏳ در حال دانلود...")
    
    # دانلود
    file_path, is_video = download_instagram(url)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                if is_video:
                    bot.send_video(message.chat.id, f)
                else:
                    bot.send_photo(message.chat.id, f)
            
            # پاک کردن فایل
            os.remove(file_path)
            os.rmdir("temp")
            bot.delete_message(message.chat.id, msg.message_id)
            
        except Exception as e:
            bot.reply_to(message, f"❌ خطا در ارسال: {e}")
    else:
        bot.reply_to(message, "❌ دانلود ناموفق! لینک رو چک کن.")

# ======== اجرا ========
if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    print("🤖 ربات روشن شد...")
    bot.infinity_polling()