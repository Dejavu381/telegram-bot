import os
import requests
from io import BytesIO
from PIL import Image  # برای تبدیل فرمت تصاویر
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیمات توکن ربات
TOKEN = "7651668912:AAG7Hi3ZzHVJrXcVxNjOhd6HJxaGcj3ffZE"

# لینک‌های دسته‌بندی
CATEGORIES = {
    "همه محصولات": "https://sadeghinasabjewelry.com/shop/",
    "دستبند": "https://sadeghinasabjewelry.com/product-category/bracelet/"
}


# تابع دانلود و تبدیل تصاویر WebP به JPG
async def fetch_and_convert_images(url):
    """دانلود تصاویر WebP و تبدیل به JPG"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        converted_files = []

        for img in images:
            img_url = img.get('src')
            if img_url and img_url.lower().endswith(".webp"):
                img_url = urljoin(url, img_url)
                filename = os.path.basename(urlparse(img_url).path)

                try:
                    img_data = requests.get(img_url, headers=headers).content
                    img_bytes = BytesIO(img_data)

                    # تبدیل تصویر از WebP به JPG
                    with Image.open(img_bytes) as img:
                        jpg_bytes = BytesIO()
                        img.convert('RGB').save(jpg_bytes, format='JPEG')
                        jpg_bytes.seek(0)

                    # ذخیره فایل JPG با نام اصلی
                    converted_files.append((jpg_bytes, filename.replace(".webp", ".jpg")))
                except Exception as e:
                    print(f"⚠️ خطا در دانلود {img_url}: {e}")

        return converted_files
    else:
        return None


# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش دکمه‌های انتخاب دسته‌بندی"""
    keyboard = [
        [InlineKeyboardButton(" همه محصولات", callback_data="همه محصولات")],
        [InlineKeyboardButton(" دستبند", callback_data="دستبند")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("دسته بندی را انتخاب کنید:", reply_markup=reply_markup)


# پردازش انتخاب دسته‌بندی و ارسال تصاویر
async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دانلود و ارسال تصاویر پس از انتخاب دسته‌بندی"""
    query = update.callback_query
    await query.answer()

    category = query.data
    url = CATEGORIES.get(category)

    if url:
        await query.edit_message_text(f"🔍 دریافت تصاویر از: {category} ...")
        images = await fetch_and_convert_images(url)

        if images:
            bot = Bot(TOKEN)
            for img_bytes, filename in images:
                img_bytes.seek(0)  # به ابتدای فایل بازگشت می‌دهیم
                await bot.send_document(chat_id=query.message.chat_id, document=img_bytes, filename=filename)
        else:
            await query.message.reply_text("⚠️ هیچ تصویر WebP پیدا نشد.")
    else:
        await query.message.reply_text("❌ دسته‌بندی نامعتبر!")


# راه‌اندازی ربات
def main():
    """اجرای ربات"""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_category_selection))

    print("🤖 ربات در حال اجراست...")
    app.run_polling()


if __name__ == "__main__":
    main()