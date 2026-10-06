import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app" / "app.py"


class DashboardSmokeTest(unittest.TestCase):
    def test_dashboard_renders_without_exceptions(self):
        result = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
        self.assertFalse(result.exception, [str(error) for error in result.exception])
        self.assertTrue(any("NBA" in title.value for title in result.title))


if __name__ == "__main__":
    unittest.main()
