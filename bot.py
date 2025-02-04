import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_glints
from dotenv import load_dotenv

# Load TOKEN dari file .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Fungsi untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Saya adalah bot pencari lowongan kerja.\n"
        "Perintah yang tersedia:\n"
        "/jobs - Melihat semua lowongan kerja terbaru.\n"
        "/cari <role> - Mencari lowongan kerja berdasarkan role tertentu.\n"
        "Saya juga akan mengirim update lowongan kerja terbaru setiap hari pukul 09:00 WIB."
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID grup ini: {chat_id}")

# Fungsi untuk menampilkan semua lowongan kerja
async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Sedang mencari lowongan kerja...")
    jobs = scrape_glints()
    if jobs:
        await update.message.reply_text("\n\n".join(jobs))
    else:
        await update.message.reply_text("❌ Tidak ada lowongan kerja terbaru saat ini.")

# Fungsi untuk mencari lowongan kerja berdasarkan role
async def cari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ Silakan masukkan role yang ingin Anda cari. Contoh: /cari developer")
        return
    
    role = " ".join(context.args).lower()
    await update.message.reply_text(f"🔍 Mencari lowongan kerja untuk role: {role}...")
    jobs = scrape_glints()
    filtered_jobs = [job for job in jobs if role in job.lower()]
    
    if filtered_jobs:
        await update.message.reply_text("\n\n".join(filtered_jobs))
    else:
        await update.message.reply_text(f"❌ Tidak ditemukan lowongan kerja untuk role: {role}")


# Fungsi untuk mengirim update otomatis ke grup
async def send_daily_updates(bot: Bot, chat_id: int):
    jobs = scrape_glints()
    if jobs:
        await bot.send_message(chat_id=chat_id, text="📢 Update Lowongan Kerja Hari Ini:\n\n" + "\n\n".join(jobs))
    else:
        await bot.send_message(chat_id=chat_id, text="📢 Update Lowongan Kerja Hari Ini:\n\n❌ Tidak ada lowongan kerja terbaru saat ini.")

if __name__ == "__main__":
    # Inisialisasi bot
    application = Application.builder().token(TOKEN).build()

    # Tambahkan command handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jobs", jobs))
    application.add_handler(CommandHandler("cari", cari))

    # ID grup Telegram (ganti dengan ID grup Anda)
    GROUP_CHAT_ID = -1001234567890  # Ganti dengan chat ID grup

    # Jadwalkan pengiriman update otomatis setiap hari pukul 09:00 WIB
    scheduler = BackgroundScheduler()
    bot_instance = application.bot  # Instance bot

    scheduler.add_job(
        send_daily_updates,
        "cron",
        hour=2,  # Waktu dalam UTC (2 UTC = 09:00 WIB)
        args=[bot_instance, GROUP_CHAT_ID],
    )
    scheduler.start()

    # Jalankan bot
    application.run_polling()
