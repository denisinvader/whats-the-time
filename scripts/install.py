#!/usr/bin/env python3
"""Install this skill into supported agent skill directories."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SKILL_NAME = "whats-the-date"
SHARED_AGENTS = ("codex", "cursor", "copilot", "gemini", "opencode")
AGENTS = (*SHARED_AGENTS, "claude", "cline", "all")


def destinations(agent: str, scope: str, project_root: Path) -> list[Path]:
    base = Path.home() if scope == "user" else project_root
    shared = base / ".agents" / "skills" / SKILL_NAME
    claude = base / ".claude" / "skills" / SKILL_NAME
    cline = base / ".cline" / "skills" / SKILL_NAME
    if agent == "all":
        return [shared, claude, cline]
    if agent == "claude":
        return [claude]
    if agent == "cline":
        return [cline]
    return [shared]


def install(targets: list[Path], source: Path, dry_run: bool) -> None:
    for target in targets:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Already exists: {target}")
    for target in targets:
        print(f"{'Would install' if dry_run else 'Installing'} {source} -> {target}")
    if dry_run:
        return
    installed: list[Path] = []
    try:
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            (target / "scripts").mkdir(parents=True)
            installed.append(target)
            shutil.copy2(source / "SKILL.md", target / "SKILL.md")
            shutil.copy2(
                source / "scripts" / "time_snapshot.py",
                target / "scripts" / "time_snapshot.py",
            )
    except OSError:
        for target in installed:
            shutil.rmtree(target)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True, choices=AGENTS)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument(
        "--project-root", type=Path, default=Path.cwd(), help="Target repository"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    source = Path(__file__).resolve().parent.parent
    targets = destinations(args.agent, args.scope, args.project_root.resolve())
    try:
        install(targets, source, args.dry_run)
    except (FileExistsError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
