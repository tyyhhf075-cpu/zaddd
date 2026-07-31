from telegram.ext import ApplicationBuilder

from config import BOT_TOKEN
from handlers import register_handlers

app = ApplicationBuilder().token(BOT_TOKEN).build()

register_handlers(app)

print("Bot is running...")
app.run_polling()