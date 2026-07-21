from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /yardim komutu
    """

    message = (
        "📖 Kullanılabilir Komutlar\n\n"
        "🏠 /start - Botu başlat\n"
        "❓ /yardim - Yardım menüsü\n"
        "⚽ /skor <takım veya lig> - Canlı maç skorları\n"
        "📅 /fikstur <takım veya lig> - Yaklaşan maçlar\n"
        "🔄 /guncelle - Takım ve lig listesini güncelle"
    )

    await update.message.reply_text(message)


def get_handler():
    return CommandHandler("yardim", help_command)