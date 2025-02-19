# Sosyal Medya Video İndirme Botu

Bu Telegram botu, çeşitli sosyal medya platformlarından video indirmenize olanak sağlar.

## Desteklenen Platformlar

- YouTube
- Instagram
- Facebook
- Twitter
- TikTok

## Kurulum

1. Python 3.8 veya daha yüksek bir sürüm yükleyin
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. `.env` dosyası oluşturun ve Telegram bot token'ınızı ekleyin:
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   ```
4. Botu çalıştırın:
   ```bash
   python bot.py
   ```

## Kullanım

1. Telegram'da botu başlatın: `/start`
2. İndirmek istediğiniz videonun linkini gönderin
3. Bot videoyu indirecek ve size gönderecektir

## Notlar

- Bazı platformlar için ek kimlik doğrulama gerekebilir
- Telif hakkı korumalı içerikleri indirmek yasaktır
- Büyük dosyalar için indirme süresi uzun olabilir 