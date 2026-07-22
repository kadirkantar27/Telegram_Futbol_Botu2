import json
from pathlib import Path
from typing import Dict, Optional, Tuple

from config import TEAMS_FILE, LEAGUES_FILE, logger
from services.football_api import FootballAPI
from utils.text import normalize

class DataManager:
    """Takım ve lig verilerini yönetir."""

    def __init__(self):
        self.team_map: Dict[str, int] = {}
        self.leagues: Dict[int, str] = {
            203: "Süper Lig",
            204: "1. Lig",
            205: "2. Lig",
            2: "UEFA Champions League",
            3: "UEFA Europa League",
            848: "UEFA Europa Conference League"
        }

    async def initialize(self):
        """
        Bot açılırken gerekli verileri yükler.
        """

        await self._load_or_update_leagues()
        await self._load_or_update_teams()

    async def _load_or_update_leagues(self):
        """
        Lig verilerini yükle.
        Dosya yoksa API'den indir.
        """

        try:

            if Path(LEAGUES_FILE).exists():

                with open(LEAGUES_FILE, "r", encoding="utf-8") as file:

                    self.leagues = {
                        int(k): v
                        for k, v in json.load(file).items()
                    }

            else:

                self.leagues = await FootballAPI.get_leagues()

                with open(LEAGUES_FILE, "w", encoding="utf-8") as file:

                    json.dump(
                        self.leagues,
                        file,
                        ensure_ascii=False,
                        indent=4
                    )

        except Exception as e:

            logger.error(f"Lig verileri yüklenemedi: {e}")
            raise

    async def _load_or_update_teams(self):
        """
        Takım verilerini yükle.
        Dosya yoksa API'den indir.
        """

        try:

            if Path(TEAMS_FILE).exists():

                with open(TEAMS_FILE, "r", encoding="utf-8") as file:

                    teams = json.load(file)

                    # Bellekte normalize edilmiş isimler tutulur
                    self.team_map = {
                        normalize(name): team_id
                        for name, team_id in teams.items()
                    }

            else:

                await self._update_all_teams()

        except Exception as e:

            logger.error(f"Takım verileri yüklenemedi: {e}")

            await self._update_all_teams()

    async def _update_all_teams(self):
        """
        Tüm Türkiye takımlarını günceller.
        """

        try:

            teams = {}

            # Liglerdeki takımlar
            for league_id in self.leagues:

                league_teams = await FootballAPI.get_league_teams(
                    league_id
                )

                teams.update(league_teams)

            # Eksik kalan Türkiye takımları
            all_teams = await FootballAPI.get_all_turkish_teams()

            teams.update(all_teams)

            # JSON'a orijinal isimlerle yaz
            with open(TEAMS_FILE, "w", encoding="utf-8") as file:

                json.dump(
                    teams,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            # Bellekte normalize edilmiş hali tutulur
            self.team_map = {
                normalize(name): team_id
                for name, team_id in teams.items()
            }

            logger.info("Takım verileri güncellendi.")

        except Exception as e:

            logger.error(f"Takımlar güncellenemedi: {e}")

            raise

    def find_league(
        self,
        user_input: str
) ->     Tuple[Optional[int], Optional[str]]:
        """
            Kullanıcının yazdığı lig adını bul.
        """

        user_input = normalize(user_input)
        aliases = {
                "sampiyonlar ligi": "UEFA Champions League",
                "champions league": "UEFA Champions League",
                "ucl": "UEFA Champions League",

                "avrupa ligi": "UEFA Europa League",
                "europa league": "UEFA Europa League",

                "konferans ligi": "UEFA Europa Conference League",
                "conference league": "UEFA Europa Conference League"
        }

        # Tam eşleşme
        for league_id, league_name in self.leagues.items():

            if normalize(league_name) == user_input:
                return league_id, league_name
        # Kısmi eşleşme
        for league_id, league_name in self.leagues.items():

            if user_input in normalize(league_name):
                return league_id, league_name

        return None, None

    def find_team(
        self,
        user_input: str
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Kullanıcının yazdığı takım adını bul.
        """

        user_input = normalize(user_input)

        # Tam eşleşme
        if user_input in self.team_map:
            return self.team_map[user_input], user_input

        # Kısmi eşleşme
        for team_name, team_id in self.team_map.items():

            if user_input in team_name:

                return team_id, team_name

        return None, None

    async def update(self):
        """
        Takım ve lig verilerini günceller.
        """

        await self._load_or_update_leagues()
        await self._update_all_teams()