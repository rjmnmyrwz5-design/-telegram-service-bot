import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or os.getenv("RENDER_EXTERNAL_URL")

TEST_VIP_USERS = {
    5525081459
}


def is_vip(user_id: int) -> bool:
    return user_id in TEST_VIP_USERS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("⭐ VIP", callback_data="vip"),
            InlineKeyboardButton("👤 حسابي", callback_data="status"),
        ],
        [
            InlineKeyboardButton("💰 الأسعار", callback_data="prices"),
        ],
    ]

    await update.message.reply_text(
        "أهلاً بك 🤖\n\n"
        "اختر الخدمة التي تريدها:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ اشتراك VIP\n\n"
        "مميزات VIP:\n"
        "• استخدام أكثر\n"
        "• أولوية في الخدمة\n"
        "• بدون قيود مستقبلية\n"
        "• ميزات حصرية\n\n"
        "💰 الأسعار:\n"
        "• شهر واحد: 5$\n"
        "• 3 أشهر: 12$\n"
        "• سنة كاملة: 35$\n\n"
        "💳 الدفع سيتم تفعيله قريباً."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_vip(user_id):
        message = (
            "⭐ حسابك VIP\n\n"
            "تم تفعيل عضوية VIP لديك."
        )
    else:
        message = (
            "👤 حسابك مجاني\n\n"
            "يمكنك الترقية إلى VIP للحصول على مميزات إضافية."
        )

    await update.message.reply_text(message)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ("vip", "prices"):
        await query.message.reply_text(
            "⭐ اشتراك VIP\n\n"
            "• استخدام أكثر\n"
            "• أولوية في الخدمة\n"
            "• ميزات حصرية\n\n"
            "💰 الأسعار:\n"
            "شهر: 5$\n"
            "3 أشهر: 12$\n"
            "سنة: 35$\n\n"
            "💳 الدفع سيتم تفعيله قريباً."
        )

    elif query.data == "status":
        if is_vip(query.from_user.id):
            await query.message.reply_text(
                "⭐ أنت مشترك VIP."
            )
        else:
            await query.message.reply_text(
                "👤 أنت على الحساب المجاني.\n\n"
                "استخدم /vip لمعرفة مميزات الاشتراك."
            )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running with webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    main()
