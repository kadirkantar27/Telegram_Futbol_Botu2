from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from services.data_manager import DataManager


class UpdateHandler:

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    async def command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """/guncelle komutu"""

        status_message = await update.message.reply_text(
            "🔄 Takım ve lig verileri güncelleniyor..."
        )

        try:

            await self.data_manager.update()

            await status_message.edit_text(
                "✅ Güncelleme tamamlandı.\n\n"
                f"🏟 Takım Sayısı : {len(self.data_manager.team_map)}\n"
                f"🏆 Lig Sayısı : {len(self.data_manager.leagues)}"
            )

        except Exception as e:

            await status_message.edit_text(
                "❌ Güncelleme başarısız!\n\n"
                f"Hata: {e}"
            )


def get_handler(data_manager: DataManager):

    return CommandHandler(
        "guncelle",
        UpdateHandler(data_manager).command
    )