import asyncio
from functools import partial
from typing import Optional, Dict, List

import requests

from config import BASE_URL, HEADERS, logger


class FootballAPI:
    """API-Football işlemleri"""

    @staticmethod
    async def fetch(endpoint: str, params: Optional[dict] = None) -> dict:
        """
        API'den veri çekmek için genel fonksiyon
        """

        loop = asyncio.get_running_loop()

        url = f"{BASE_URL}/{endpoint}"

        func = partial(
            requests.get,
            url,
            headers=HEADERS,
            params=params
        )

        try:
            response = await loop.run_in_executor(None, func)

            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"API isteği başarısız: {e}")
            raise

    @classmethod
    async def get_all_turkish_teams(cls) -> Dict[str, int]:
        """
        Türkiye'deki bütün takımları getir
        """

        data = await cls.fetch(
            "teams",
            {
                "country": "Turkey"
            }
        )

        return {
            team["team"]["name"].lower(): team["team"]["id"]
            for team in data.get("response", [])
        }

    @classmethod
    async def get_league_teams(cls, league_id: int) -> Dict[str, int]:
        """
        Belirli ligdeki takımları getir
        """
        from datetime import datetime

        now = datetime.now()
        # Temmuz (7. ay) ve sonrasındaysak bulunduğumuz yıl, değilse bir önceki yıl sezondur.
        current_season = now.year if now.month >= 7 else now.year - 1

        data = await cls.fetch(
            "teams",
            {
                "league": league_id,
                "season": current_season
            }
        )

        return {
            team["team"]["name"].lower(): team["team"]["id"]
            for team in data.get("response", [])
        }

    @classmethod
    async def get_leagues(cls) -> Dict[int, str]:
        """
        Türkiye liglerini getir
        """

        data = await cls.fetch(
            "leagues",
            {
                "country": "Turkey"
            }
        )

        return {
            league["league"]["id"]: league["league"]["name"]
            for league in data.get("response", [])
        }

    @classmethod
    async def get_live_matches(
        cls,
        team_id: Optional[int] = None,
        league_id: Optional[int] = None
    ) -> List[dict]:
        """
        Canlı maçları getir
        """

        params = {
            "live": "all"
        }

        if team_id:
            params["team"] = team_id

        if league_id:
            params["league"] = league_id

        data = await cls.fetch(
            "fixtures",
            params
        )

        return data.get("response", [])
    

    @classmethod
    async def get_fixtures(
        cls,
        team_id: Optional[int] = None,
        league_id: Optional[int] = None
    ) -> List[dict]:
        """
        Yaklaşan maçları getir
        """
        from datetime import datetime
        
        now = datetime.now()
        # Temmuz veya sonrasındaysak yeni sezon (örn: 2026), değilse geçen sezon
        current_season = now.year if now.month >= 7 else now.year - 1

        params = {
            "next": 5,
            "timezone": "Europe/Istanbul",
            "season": current_season  # API'yi yeni sezona bakmaya zorluyoruz
        }

        if team_id:
            params["team"] = team_id

        if league_id:
            params["league"] = league_id

        data = await cls.fetch(
            "fixtures",
            params
        )

        return data.get("response", [])
    

    @classmethod
    async def get_turkish_live_scores(cls) -> List[dict]:
        """
        Türkiye liglerindeki canlı maçları getir
        """
        matches = []
        for league_id in [203, 204, 205]:
             data = await cls.fetch(
            "fixtures",
            {
                "league": league_id,
                "live": "all"
            }
        )

        matches.extend(data.get("response", []))
        return matches
    
    