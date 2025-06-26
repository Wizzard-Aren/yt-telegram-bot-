from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp
import os
import asyncio

# ✅ Read token from environment variable (do NOT hardcode)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Send me a video link!")

async def handle_message(update, context):
    url = update.message.text
    await update.message.reply_text("Downloading...")

    try:
        ydl_opts = {'outtmpl': '%(title)s.%(ext)s', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(file_name, 'rb'))
        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()

