import os
import google.generativeai as genai
from telebot import TeleBot

# ======== دریافت توکن‌ها از محیط ========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN پیدا نشد! توی Render تنظیمش کن.")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY پیدا نشد! توی Render تنظیمش کن.")

bot = TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# ======== شخصیت متخصص اینستاگرام ========
PERSONALITY = """تو یک متخصص حرفه‌ای تولید محتوای اینستاگرام هستی با ۱۰ سال سابقه.

ویژگی‌های تو:
- استراتژی‌های عملی و کاربردی ارائه می‌دی
- کپشن‌های جذاب و فروشنده می‌نویسی (۳ سبک مختلف: عاطفی، فروشنده، طنز)
- هشتگ‌های طلایی و پرسرچ معرفی می‌کنی (۳۰ تا: ۱۰ پرسرچ، ۱۰ متوسط، ۱۰ اختصاصی)
- ایده‌های خلاقانه برای ریلز و استوری می‌دی (۵ ایده متنوع)
- ساده و صمیمی صحبت می‌کنی، نه خشک و آکادمیک
- همیشه از مثال واقعی و کاربردی استفاده می‌کنی
- با ایموجی و لحن دوستانه جواب می‌دی
- هیچوقت جواب‌های کلی و تکراری نمی‌دی

مهم: همیشه جواب‌هات رو دسته‌بندی و منظم بنویس تا کاربر راحت بخونه.
"""

model = genai.GenerativeModel('gemini-1.5-flash')

# ======== تابع ارسال به جمنای ========
def ask_gemini(prompt):
    try:
        response = model.generate_content(f"{PERSONALITY}\n\nدرخواست کاربر:\n{prompt}")
        return response.text[:4000]  # محدودیت تلگرام
    except Exception as e:
        return f"❌ خطا در ارتباط با جمنای: {e}"

# ======== دستور استارت ========
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "📱 **به مشاور تولید محتوای اینستاگرام خوش اومدی!**\n\n"
        "از من بپرس:\n"
        "• `/idea موضوع` → ایده برای پست/ریلز\n"
        "• `/caption موضوع` → کپشن حرفه‌ای\n"
        "• `/hashtag موضوع` → هشتگ‌های طلایی\n"
        "• `/strategy نوع پیج` → استراتژی رشد\n"
        "• `/analyze توضیح پیج` → تحلیل محتوا\n\n"
        "یا هر سوالی داری، مستقیم بپرس! 🚀"
    )

# ======== راهنما ========
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
        "📚 **راهنمای استفاده:**\n\n"
        "`/idea [موضوع]` → ۵ ایده خلاقانه\n"
        "`/caption [موضوع]` → ۳ کپشن جذاب\n"
        "`/hashtag [موضوع]` → ۳۰ هشتگ طلایی\n"
        "`/strategy [نوع پیج]` → برنامه ۳۰ روزه رشد\n"
        "`/analyze [توضیح پیج]` → تحلیل نقاط قوت/ضعف\n\n"
        "مثال: `/idea مد لباس`"
    )

# ======== ایده ========
@bot.message_handler(commands=['idea'])
def get_idea(message):
    topic = message.text.replace('/idea', '').strip()
    if not topic:
        bot.reply_to(message, "❌ موضوع رو مشخص کن!\nمثال: `/idea مد لباس`")
        return
    msg = bot.reply_to(message, "⏳ در حال تولید ایده...")
    result = ask_gemini(f"برای موضوع '{topic}'، ۵ ایده خلاقانه برای ریلز و پست بده.")
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# ======== کپشن ========
@bot.message_handler(commands=['caption'])
def get_caption(message):
    topic = message.text.replace('/caption', '').strip()
    if not topic:
        bot.reply_to(message, "❌ موضوع رو مشخص کن!\nمثال: `/caption قهوه صبح`")
        return
    msg = bot.reply_to(message, "⏳ در حال نوشتن کپشن...")
    result = ask_gemini(f"برای موضوع '{topic}'، ۳ کپشن جذاب با سبک‌های عاطفی، فروشنده و طنز بنویس.")
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# ======== هشتگ ========
@bot.message_handler(commands=['hashtag'])
def get_hashtag(message):
    topic = message.text.replace('/hashtag', '').strip()
    if not topic:
        bot.reply_to(message, "❌ موضوع رو مشخص کن!\nمثال: `/hashtag فیتنس`")
        return
    msg = bot.reply_to(message, "⏳ در حال تولید هشتگ...")
    result = ask_gemini(f"برای موضوع '{topic}'، ۳۰ هشتگ طلایی (۱۰ پرسرچ، ۱۰ متوسط، ۱۰ اختصاصی) بده.")
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# ======== استراتژی ========
@bot.message_handler(commands=['strategy'])
def get_strategy(message):
    topic = message.text.replace('/strategy', '').strip()
    if not topic:
        bot.reply_to(message, "❌ نوع پیج رو مشخص کن!\nمثال: `/strategy پیج آشپزی`")
        return
    msg = bot.reply_to(message, "⏳ در حال طراحی استراتژی...")
    result = ask_gemini(f"برای یه پیج '{topic}'، یه استراتژی ۳۰ روزه برای رشد و افزایش تعامل ارائه بده.")
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# ======== تحلیل ========
@bot.message_handler(commands=['analyze'])
def analyze(message):
    topic = message.text.replace('/analyze', '').strip()
    if not topic:
        bot.reply_to(message, "❌ توضیح پیج رو بده!\nمثال: `/analyze پیج فلان`")
        return
    msg = bot.reply_to(message, "⏳ در حال تحلیل...")
    result = ask_gemini(f"این پیج رو تحلیل کن: {topic}\nنقاط قوت، ضعف، و راهکارهای بهبود رو بگو.")
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# ======== پیام‌های معمولی ========
@bot.message_handler(func=lambda m: True)
def chat(message):
    msg = bot.reply_to(message, "⏳ در حال فکر کردن...")
    result = ask_gemini(message.text)
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# ======== اجرا ========
if __name__ == "__main__":
    print("🤖 ربات مشاور اینستاگرام روشن شد...")
    bot.infinity_polling()
