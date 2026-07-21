from datetime import datetime


class Formatter:
    """Telegram mesajlarını oluşturan yardımcı sınıf."""

    @staticmethod
    def team_not_found(name: str) -> str:
        return (
            f"❌ '{name}' isminde bir takım bulunamadı.\n\n"
            "Takım adını tekrar kontrol edip yeniden deneyin."
        )

    @staticmethod
    def no_live_matches() -> str:
        return "📺 Şu anda oynanan canlı maç bulunmuyor."

    @staticmethod
    def no_fixtures() -> str:
        return "📅 Yaklaşan maç bulunamadı."

    @staticmethod
    def update_success(team_count: int, league_count: int) -> str:
        return (
            "✅ Veriler başarıyla güncellendi.\n\n"
            f"🏟 Takım Sayısı : {team_count}\n"
            f"🏆 Lig Sayısı : {league_count}"
        )

    @staticmethod
    def format_live_match(match: dict) -> str:
        fixture = match["fixture"]
        teams = match["teams"]
        goals = match["goals"]

        elapsed = fixture["status"].get("elapsed") or 0

        return (
            f"🏆 {match['league']['name']}\n"
            f"⚽ {teams['home']['name']} {goals['home']} - {goals['away']} {teams['away']['name']}\n"
            f"⏱ {elapsed}'"
        )

    @staticmethod
    def format_fixture(match: dict) -> str:
        fixture = match["fixture"]
        teams = match["teams"]

        date = datetime.fromisoformat(
            fixture["date"].replace("Z", "+00:00")
        )

        return (
            f"🏆 {match['league']['name']}\n"
            f"⚽ {teams['home']['name']} - {teams['away']['name']}\n"
            f"📅 {date.strftime('%d.%m.%Y')}\n"
            f"🕒 {date.strftime('%H:%M')}"
        )

    @staticmethod
    def format_live_matches(matches: list) -> str:
        if not matches:
            return Formatter.no_live_matches()

        return "\n\n".join(
            Formatter.format_live_match(match)
            for match in matches
        )

    @staticmethod
    def format_fixtures(matches: list) -> str:
        if not matches:
            return Formatter.no_fixtures()

        return "\n\n".join(
            Formatter.format_fixture(match)
            for match in matches
        )