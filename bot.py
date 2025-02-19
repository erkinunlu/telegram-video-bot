import os
import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
from dotenv import load_dotenv

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# .env dosyasından değişkenleri yükle
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

def is_tiktok_url(url: str) -> bool:
    return 'tiktok.com' in url.lower()

# Video indirme fonksiyonu
async def download_video(url: str) -> str:
    base_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'no_warnings': True,
        'quiet': True,
    }
    
    if is_tiktok_url(url):
        # TikTok için özel ayarlar
        ydl_opts = {
            **base_opts,
            'format': 'best',
            'cookiesfrombrowser': ('chrome',),  # Tarayıcıdan çerezleri al
            'extractor_args': {
                'tiktok': {
                    'embed_url': True,
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    'app_version': '1.0.0',
                    'use_api': True
                }
            }
        }
    else:
        # Diğer platformlar için ayarlar
        ydl_opts = {
            **base_opts,
            'username': INSTAGRAM_USERNAME,
            'password': INSTAGRAM_PASSWORD,
            'cookiefile': 'cookies.txt',
            'extract_flat': False,
            'mark_watched': False,
            'ignoreerrors': False
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{info['title']}.{info['ext']}"
    except Exception as e:
        logging.error(f"Video indirme hatası: {str(e)}")
        if "login required" in str(e).lower():
            raise Exception("Instagram girişi gerekiyor. Lütfen bot yöneticisiyle iletişime geçin.")
        elif "Unable to extract sigi state" in str(e):
            raise Exception("TikTok video indirme hatası. Alternatif yöntem deneniyor...")
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
        error_msg = str(e)
        if "TikTok video indirme hatası" in error_msg:
            await message.reply_text("TikTok videosunu indirirken bir sorun oluştu. "
                                   "Lütfen videonun herkese açık olduğundan emin olun.")
        else:
            await message.reply_text(f"Üzgünüm, bir hata oluştu: {error_msg}")

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