# What's the Date?

Ask an agent “What day is it?” and you may get a date from its prompt or from memory. Neither is a clock. This skill tells the agent to read the machine's clock when the question is about **now**, then answer with the right calendar field and time zone.

It works locally, uses Python's standard library, and sends nothing over the network. The same skill files run on Windows, macOS, and Linux.

## Try it

Python 3.9 or newer is required. Clone this repository, then install the skill for your user account:

```sh
python3 scripts/install.py --agent all
```

On Windows, run the same installer with the Python launcher:

```powershell
py -3 scripts/install.py --agent all
```

`all` installs three copies: one in `~/.agents/skills/whats-the-date` for Codex, Cursor, GitHub Copilot, Gemini CLI, and OpenCode; one in `~/.claude/skills/whats-the-date` for Claude Code; and one in `~/.cline/skills/whats-the-date` for Cline. Use `--agent` with a single harness name if you only want its location. The installer checks every destination before writing and leaves an existing installation alone. Run it with `--dry-run` to see the paths first.

For a single repository, pass `--scope project --project-root /path/to/project`. On Windows, a path such as `C:\work\my-project` works. The default scope is `user`; the default project root is the current working directory.

Restart your agent session if the skill does not appear. Then ask:

> What year is it?
>
> What day of the week is it in Tokyo?
>
> Give me the current date and time in UTC.

You can also call the skill explicitly as `whats-the-date` in a harness that supports skill commands.

## What it reads

The bundled script takes one clock reading and prints JSON. Run it directly to check what the agent will see:

```sh
python3 scripts/time_snapshot.py
python3 scripts/time_snapshot.py --timezone UTC
python3 scripts/time_snapshot.py --timezone Europe/Paris
```

On Windows, replace `python3` with `py -3`. A snapshot contains `iso`, `date`, `time`, `year`, `month`, `month_name`, `day`, `weekday` (Monday is 1), `weekday_name`, `timezone`, and `utc_offset`. The default is the host's local time zone. Times are reported to the second.

For named IANA time zones, Python needs a time zone database. macOS and Linux usually provide one through the OS. Some Windows Python installations need `py -3 -m pip install tzdata`. UTC and the local time zone work without that optional package. A wrong system clock or incorrect host time-zone setting will produce a wrong answer; this skill cannot verify either against an external clock.

## Where the files go

| Harness | Project skill directory | User skill directory |
| --- | --- | --- |
| Codex | `.agents/skills/whats-the-date/` | `~/.agents/skills/whats-the-date/` |
| Cursor | `.agents/skills/whats-the-date/` | `~/.agents/skills/whats-the-date/` |
| GitHub Copilot | `.agents/skills/whats-the-date/` | `~/.agents/skills/whats-the-date/` |
| Gemini CLI | `.agents/skills/whats-the-date/` | `~/.agents/skills/whats-the-date/` |
| OpenCode | `.agents/skills/whats-the-date/` | `~/.agents/skills/whats-the-date/` |
| Claude Code | `.claude/skills/whats-the-date/` | `~/.claude/skills/whats-the-date/` |
| Cline | `.cline/skills/whats-the-date/` | `~/.cline/skills/whats-the-date/` |

Each installed directory contains `SKILL.md` and `scripts/time_snapshot.py`. You can copy those two files by hand into another agent's skill directory if it follows the [Agent Skills format](https://agentskills.io/). An agent without skill discovery can still read `SKILL.md` as instructions and run the script. Skill discovery and shell execution depend on the harness and its permissions.

The paths above follow the current documentation for [Codex](https://learn.chatgpt.com/docs/build-skills), [Cursor](https://cursor.com/docs/skills), [GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/), [OpenCode](https://docs.opencode.ai/docs/skills/), [Claude Code](https://code.claude.com/docs/en/skills), and [Cline](https://docs.cline.bot/customization/skills).

## Update or remove

Pull the latest repository version, remove the installed `whats-the-date` directory, and run the installer again. To uninstall, remove that directory from the path shown in the table. The installer never edits an agent's global configuration.

## Development

Run the checks locally with `python3 -m unittest discover -s tests -v`, `ruff check .`, and `ruff format --check .`. GitHub Actions runs those checks on Windows, macOS, and Linux. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution process and [SECURITY.md](SECURITY.md) for reporting a security issue.

Licensed under [MIT](LICENSE).
