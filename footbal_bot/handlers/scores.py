from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from services.football_api import FootballAPI
from services.data_manager import DataManager
from utils.formatter import Formatter
from utils.search import resolve_query


class ScoresHandler:

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    async def command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """/skor komutu"""
        if not context.args:
            matches = await FootballAPI.get_live_matches()

            turkish_team_ids = set(self.data_manager.team_map.values())

            turkish_matches = []
            for match in matches:
                home_id = match["teams"]["home"]["id"]
                away_id = match["teams"]["away"]["id"]
                if home_id in turkish_team_ids or away_id in turkish_team_ids:
                    turkish_matches.append(match)

            if not turkish_matches:
                await update.message.reply_text(
                    "🇹🇷 Şu anda Türk takımlarının canlı maçı bulunmuyor."
                )
                return

            await update.message.reply_text(
                Formatter.format_live_matches(turkish_matches)
            )
            return

        query = " ".join(context.args)

        team_id, league_id, query = resolve_query(
            query,
            self.data_manager
        )

        if team_id:
            matches = await FootballAPI.get_live_matches(
                team_id=team_id
            )
            await update.message.reply_text(
                Formatter.format_live_matches(matches)
            )
            return

        if league_id:
            matches = await FootballAPI.get_live_matches(
                league_id=league_id
            )
            await update.message.reply_text(
                Formatter.format_live_matches(matches)
            )
            return

        await update.message.reply_text(
            Formatter.team_not_found(query)
        )


def get_handler(data_manager: DataManager):

    return CommandHandler(
        "skor",
        ScoresHandler(data_manager).command
    )