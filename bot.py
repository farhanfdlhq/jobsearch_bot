from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
from scraper import scrape_glints

# Load token dari file .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Fungsi untuk handle command /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Halo! Saya bot pencari lowongan kerja. Gunakan /jobs untuk melihat lowongan terbaru.")
    # Jadwalkan pengiriman otomatis ke pengguna
    chat_id = update.message.chat_id
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_send_jobs, 'interval', hours=6, args=[context])
    scheduler.start()

# Fungsi untuk handle command /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Perintah yang tersedia:\n/jobs - Cari lowongan kerja")

# Fungsi untuk handle command /jobs
def send_jobs(update: Update, context: CallbackContext):
    jobs = scrape_glints()
    if jobs:
        update.message.reply_text("Lowongan terbaru di Glints:\n\n" + "\n".join(jobs))
    else:
        update.message.reply_text("Maaf, tidak ada lowongan yang ditemukan.")

# Fungsi untuk mengirim update otomatis
def auto_send_jobs(context: CallbackContext):
    jobs = scrape_glints()
    if jobs:
        context.bot.send_message(
            chat_id=context.job.context,
            text="🔄 Update Lowongan Glints:\n\n" + "\n".join(jobs)
        )

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("jobs", send_jobs))

    updater.start_polling()
    updater.idle()