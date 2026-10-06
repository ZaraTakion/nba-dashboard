import unittest

import pandas as pd

from app.data_utils import load_data, prepare_data


class PrepareDataTests(unittest.TestCase):
    def frame(self, teams, seasons=None, percentages=None):
        count = len(teams)
        return pd.DataFrame(
            {
                "Team": teams,
                "Season": seasons or [2023] * count,
                "PTS": [110.0] * count,
                "AST": [25.0] * count,
                "TRB": [44.0] * count,
                "STL": [7.0] * count,
                "BLK": [5.0] * count,
                "TOV": [13.0] * count,
                "FG_Percent": percentages or [0.47] * count,
                "3P_Percent": [0.36] * count,
                "2P_Percent": [0.54] * count,
                "FT_Percent": [0.78] * count,
            }
        )

    def test_historical_aliases_preserve_source_label_and_marker(self):
        source = self.frame(
            ["Seattle SuperSonics*", "Oklahoma City Thunder", "New Jersey Nets"]
        )
        # The two Seattle/OKC labels are deliberately in different seasons.
        source.loc[1, "Season"] = 2009
        result = prepare_data(source)
        seattle = result.loc[result["Source_Team"].eq("Seattle SuperSonics")].iloc[0]
        self.assertEqual(seattle["Franchise"], "Oklahoma City Thunder")
        self.assertTrue(seattle["Playoffs"])
        self.assertEqual(seattle["Source_Team"], "Seattle SuperSonics")
        self.assertFalse(result["Is_League_Average"].any())

    def test_csv_is_valid_and_season_labels_are_complete(self):
        data = load_data()
        self.assertEqual(len(data), 739)
        self.assertEqual(sorted(data["Season"].unique()), list(range(2000, 2024)))
        self.assertEqual(data.loc[data["Is_League_Average"]].shape[0], 24)
        team_rows = data.loc[~data["Is_League_Average"]]
        self.assertFalse(team_rows.duplicated(["Franchise", "Season"]).any())
        for column in ("FG_Percent", "3P_Percent", "2P_Percent", "FT_Percent"):
            self.assertTrue(team_rows[column].between(0, 1).all())

    def test_rejects_missing_required_columns(self):
        source = self.frame(["Boston Celtics"]).drop(columns="AST")
        with self.assertRaisesRegex(ValueError, "AST"):
            prepare_data(source)

    def test_rejects_invalid_percentage_scale(self):
        source = self.frame(["Boston Celtics"], percentages=[47.0])
        with self.assertRaisesRegex(ValueError, "entre 0 e 1"):
            prepare_data(source)

    def test_rejects_duplicate_franchise_season_after_aliasing(self):
        source = self.frame(["Charlotte Bobcats", "Charlotte Hornets"])
        with self.assertRaisesRegex(ValueError, "mesma franquia e temporada"):
            prepare_data(source)

    def test_rejects_non_numeric_stats(self):
        source = self.frame(["Boston Celtics"])
        source["PTS"] = source["PTS"].astype(object)
        source.loc[0, "PTS"] = "n/a"
        with self.assertRaisesRegex(ValueError, "PTS"):
            prepare_data(source)


if __name__ == "__main__":
    unittest.main()
