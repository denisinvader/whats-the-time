import tempfile
import unittest
from pathlib import Path

from scripts.install import destinations, install


class InstallerTests(unittest.TestCase):
    def test_all_project_paths(self):
        root = Path("example-project")
        paths = destinations("all", "project", root)
        self.assertEqual(paths[0], root / ".agents/skills/whats-the-date")
        self.assertEqual(paths[1], root / ".claude/skills/whats-the-date")
        self.assertEqual(paths[2], root / ".cline/skills/whats-the-date")

    def test_install_copies_only_skill_files_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path(__file__).resolve().parents[1]
            paths = destinations("all", "project", root)
            install(paths, source, dry_run=False)
            for path in paths:
                self.assertEqual(
                    sorted(p.relative_to(path).as_posix() for p in path.rglob("*")),
                    ["SKILL.md", "scripts", "scripts/time_snapshot.py"],
                )
            with self.assertRaises(FileExistsError):
                install(paths, source, dry_run=False)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = destinations("all", "project", root)
            install(paths, Path(__file__).resolve().parents[1], dry_run=True)
            self.assertTrue(all(not path.exists() for path in paths))


if __name__ == "__main__":
    unittest.main()
