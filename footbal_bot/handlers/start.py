from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start komutu"""

    text = (
        "👋 Merhaba!\n\n"
        "Senin için:\n"
        "• Türk takımlarının Canlı maç skorlarını gösterebilirim.\n"
        "• Takım ve lig verilerini güncelleyebilirim.\n\n"
        "📋 Kullanılabilir Komutlar\n\n"
        "🏠 /start - Botu başlat\n"
        "❓ /yardim - Yardım menüsü\n"
        "⚽ /skor <takım veya lig>\n"
        "🔄 /guncelle\n\n"
        "Örnekler:\n"
        "`/skor galatasaray`\n"
        "`/skor süper lig`"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )


def get_handler():
    """Start handler'ını döndürür."""
    return CommandHandler("start", start)