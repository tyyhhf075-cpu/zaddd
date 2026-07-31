from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from database import add_user
from states import WAITING_MESSAGE

TARGET_ID = "target_id"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)

    bot_username = (await context.bot.get_me()).username

    # إذا دخل من رابط خاص
    if context.args:
        try:
            target_id = int(context.args[0])

            if target_id == user.id:
                await update.message.reply_text("❌ لا يمكنك إرسال رسالة مجهولة لنفسك.")
                return ConversationHandler.END

            context.user_data[TARGET_ID] = target_id

            await update.message.reply_text(
                "✍️ اكتب رسالتك المجهولة الآن:"
            )

            return WAITING_MESSAGE

        except ValueError:
            pass

    # /start العادي
    link = f"https://t.me/{bot_username}?start={user.id}"

    await update.message.reply_text(
    f"""👋 أهلاً بك {user.first_name} في ZAD Anonymous Bot

استقبل الرسائل المجهولة بكل سهولة وخصوصية تامة.

📩 شارك رابطك مع أصدقائك، وسيتمكن أي شخص من إرسال رسالة إليك دون الكشف عن هويته.

🔒 جميع الرسائل تُنقل عبر اتصال آمن ومشفّر لحماية بياناتك وخصوصيتك.

━━━━━━━━━━━━━━━

🔗 رابطك الخاص:

{link}

━━━━━━━━━━━━━━━

⚡ تم تطوير هذا البوت بواسطة ZAD."""
)

    return ConversationHandler.END


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_id = context.user_data.get(TARGET_ID)

    if not target_id:
        return ConversationHandler.END

    text = update.message.text

    await context.bot.send_message(
        chat_id=target_id,
        text=f"📩 لديك رسالة مجهولة:\n\n{text}"
    )

    await update.message.reply_text("✅ تم إرسال رسالتك بنجاح.")

    context.user_data.clear()

    return ConversationHandler.END


def register_handlers(app):
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)
            ]
        },
        fallbacks=[],
    )

    app.add_handler(conv)