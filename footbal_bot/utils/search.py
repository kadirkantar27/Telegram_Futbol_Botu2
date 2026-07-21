from typing import Optional, Tuple
from utils.text import normalize
from services.data_manager import DataManager

def normalize(text: str) -> str:
    """
    Arama yapılacak metni normalize eder.
    """

    replacements = str.maketrans({
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    })

    return text.lower().translate(replacements).strip()

def resolve_query(query, data_manager):
    """
    Önce takım, sonra lig arar.
    """

    query = normalize(query)

    team_id, team_name = data_manager.find_team(query)

    if team_id:
        return team_id, None, team_name

    league_id, league_name = data_manager.find_league(query)

    if league_id:
        return None, league_id, league_name

    return None, None, query