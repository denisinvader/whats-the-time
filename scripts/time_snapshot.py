#!/usr/bin/env python3
"""Read one current instant and print a portable date/time snapshot."""

from __future__ import annotations

import argparse
import calendar
import json
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def resolve_timezone(name: str | None):
    if name is None:
        return None
    if name.upper() == "UTC":
        return timezone.utc
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(
            f"Time zone {name!r} is unavailable. Check the IANA name; "
            "on Windows, install the Python 'tzdata' package if zone data is missing."
        ) from exc


def snapshot(now: datetime, zone_name: str | None) -> dict[str, str | int]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("snapshot requires a timezone-aware datetime")
    return {
        "iso": now.isoformat(timespec="seconds"),
        "date": now.date().isoformat(),
        "time": now.time().isoformat(timespec="seconds"),
        "year": now.year,
        "month": now.month,
        "month_name": calendar.month_name[now.month],
        "day": now.day,
        "weekday": now.isoweekday(),
        "weekday_name": calendar.day_name[now.weekday()],
        "timezone": zone_name or now.tzname() or "local",
        "utc_offset": now.strftime("%z")[:3] + ":" + now.strftime("%z")[3:],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timezone", help="IANA time zone (for example Europe/Paris) or UTC"
    )
    args = parser.parse_args(argv)
    try:
        zone = resolve_timezone(args.timezone)
        now = datetime.now(zone) if zone is not None else datetime.now().astimezone()
        zone_name = (
            "UTC" if args.timezone and args.timezone.upper() == "UTC" else args.timezone
        )
        result = snapshot(now, zone_name)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
