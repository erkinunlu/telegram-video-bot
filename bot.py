import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
from dotenv import load_dotenv

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# .env dosyasından TOKEN'ı yükle
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Video indirme fonksiyonu
async def download_video(url: str) -> str:
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'no_warnings': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{info['title']}.{info['ext']}"
    except Exception as e:
        logging.error(f"Video indirme hatası: {str(e)}")
        raise e

# Başlangıç komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ben sosyal medya video indirme botuyum. "
        "Instagram, Facebook, Twitter, YouTube ve TikTok linklerini bana gönderebilirsin."
    )

# Link işleme
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    url = message.text

    await message.reply_text("Video indiriliyor, lütfen bekleyin...")
    
    try:
        video_path = await download_video(url)
        
        # Videoyu gönder
        with open(video_path, 'rb') as video_file:
            await message.reply_video(
                video=video_file,
                caption="İşte videonuz! 🎥"
            )
            
        # Temizlik
        os.remove(video_path)
        
    except Exception as e:
        await message.reply_text(f"Üzgünüm, bir hata oluştu: {str(e)}")

def main():
    # Bot uygulamasını oluştur
    application = Application.builder().token(TOKEN).build()

    # Komut işleyicilerini ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

    # Botu başlat
    application.run_polling()

if __name__ == '__main__':
    main() 