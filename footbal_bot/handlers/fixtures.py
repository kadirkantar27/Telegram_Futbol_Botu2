from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from services.football_api import FootballAPI
from services.data_manager import DataManager
from utils.formatter import Formatter
from utils.search import resolve_query


class FixturesHandler:

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    async def command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """/fikstur komutu"""

        # Parametre verilmediyse tüm yaklaşan maçlar
        if not context.args:

            matches = await FootballAPI.get_fixtures()

            await update.message.reply_text(
                Formatter.format_fixtures(matches)
            )

            return

        query = " ".join(context.args)

        team_id, league_id, query = resolve_query(
            query,
            self.data_manager
        )

        if team_id:

            matches = await FootballAPI.get_fixtures(
                team_id=team_id
            )

            await update.message.reply_text(
                Formatter.format_fixtures(matches)
            )

            return

        if league_id:

            matches = await FootballAPI.get_fixtures(
                league_id=league_id
            )

            await update.message.reply_text(
                Formatter.format_fixtures(matches)
            )

            return

        await update.message.reply_text(
            Formatter.team_not_found(query)
        )


def get_handler(data_manager: DataManager):

    return CommandHandler(
        "fikstur",
        FixturesHandler(data_manager).command
    )