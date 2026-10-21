import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.time_snapshot import resolve_timezone, snapshot

ROOT = Path(__file__).resolve().parents[1]


class SnapshotTests(unittest.TestCase):
    def test_calendar_fields_at_year_boundary(self):
        instant = datetime(2027, 1, 1, 0, 30, tzinfo=timezone(timedelta(hours=3)))
        result = snapshot(instant, "Europe/Moscow")
        self.assertEqual(result["date"], "2027-01-01")
        self.assertEqual(result["year"], 2027)
        self.assertEqual(result["month"], 1)
        self.assertEqual(result["weekday"], 5)
        self.assertEqual(result["weekday_name"], "Friday")
        self.assertEqual(result["utc_offset"], "+03:00")
        self.assertEqual(result["iso"], "2027-01-01T00:30:00+03:00")

    def test_negative_half_hour_offset(self):
        instant = datetime(
            2026, 6, 1, 1, 2, tzinfo=timezone(-timedelta(hours=3, minutes=30))
        )
        self.assertEqual(snapshot(instant, None)["utc_offset"], "-03:30")

    def test_naive_datetime_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            snapshot(datetime(2026, 1, 1), None)

    def test_utc_needs_no_zone_database(self):
        self.assertIs(resolve_timezone("utc"), timezone.utc)

    def test_cli_returns_current_utc_snapshot(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "time_snapshot.py"),
                "--timezone",
                "UTC",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        result = json.loads(proc.stdout)
        self.assertEqual(result["timezone"], "UTC")
        self.assertEqual(result["utc_offset"], "+00:00")
        self.assertEqual(result["date"], result["iso"][:10])

    def test_cli_normalizes_utc_label(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "time_snapshot.py"),
                "--timezone",
                "utc",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(proc.stdout)["timezone"], "UTC")

    def test_cli_reports_unknown_zone(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "time_snapshot.py"),
                "--timezone",
                "No/Such_Zone",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unavailable", proc.stderr)
        self.assertEqual(proc.stdout, "")


if __name__ == "__main__":
    unittest.main()
