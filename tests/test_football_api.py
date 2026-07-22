import unittest

from services.football_api import FootballAPI


class FootballAPITests(unittest.TestCase):
    def test_build_fixture_params_for_team_includes_future_status(self):
        params = FootballAPI._build_fixture_params(team_id=102)

        self.assertEqual(params["team"], 102)
        self.assertEqual(params["next"], 10)
        self.assertEqual(params["status"], "NS")
        self.assertEqual(params["timezone"], "Europe/Istanbul")


if __name__ == "__main__":
    unittest.main()
