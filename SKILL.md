---
name: whats-the-date
description: Get the current date or time from the running machine. Use when a user asks what year, month, date, day of the week, or time it is now, including questions that specify a time zone. Do not use for historical dates or date arithmetic.
license: MIT
---

# What's the Date?

Use the bundled clock script for questions about **now**. A date in the conversation, a system prompt, or a model's memory may be stale. Read the clock when answering, as close to the response as practical.

## Read the clock

Run `scripts/time_snapshot.py` from this skill's installed directory with Python 3.9 or newer. In the examples below, `<skill-directory>` means the folder containing this `SKILL.md`. Use `python3` on macOS and Linux; on Windows use `py -3` or `python`. If your harness provides a trusted current-time tool, you may use it instead.

```text
python3 <skill-directory>/scripts/time_snapshot.py
python3 <skill-directory>/scripts/time_snapshot.py --timezone UTC
python3 <skill-directory>/scripts/time_snapshot.py --timezone Europe/Paris
```

The JSON output captures one instant and includes the local calendar date, clock time, weekday, ISO 8601 timestamp, UTC offset, and time-zone label. The default is the machine's local time zone. For an explicitly requested IANA zone, pass `--timezone`; if zone data is missing, follow the script's error message. Never guess a requested zone's current offset.

Answer only what the user asked for, in the user's language. Include the time zone or UTC offset when giving a time, or when the date could differ across zones. If the user names a place but its time zone is ambiguous, ask which zone they mean. If the clock cannot be read, say so rather than presenting a remembered date as current.
