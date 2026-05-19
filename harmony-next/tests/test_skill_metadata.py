from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parent
SKILL_PATH = SKILL_ROOT / "SKILL.md"
README_PATH = REPO_ROOT / "README.md"
README_EN_PATH = REPO_ROOT / "README_en.md"
SCRIPT_ROOT = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

import sync_release_version  # noqa: E402


class SkillMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = SKILL_PATH.read_text(encoding="utf-8")
        self.readme_text = README_PATH.read_text(encoding="utf-8")
        self.readme_en_text = README_EN_PATH.read_text(encoding="utf-8")

    def test_skill_exposes_current_version_for_agents(self) -> None:
        metadata_version = re.search(r"version:\s*\"(\d+\.\d+\.\d+)\"", self.skill_text)
        visible_version = re.search(r"Current local skill version:\s*`v\d+\.\d+\.\d+`", self.skill_text)
        hidden_version = re.search(r"<!-- version:\s*(\d+\.\d+\.\d+)\s*-->", self.skill_text)

        self.assertIsNotNone(metadata_version)
        self.assertIsNotNone(visible_version)
        self.assertIsNotNone(hidden_version)
        self.assertEqual(metadata_version.group(1), hidden_version.group(1))
        self.assertIn(f"`v{metadata_version.group(1)}`", visible_version.group(0))

    def test_readme_release_badges_match_skill_version(self) -> None:
        metadata_version = re.search(r"version:\s*\"(\d+\.\d+\.\d+)\"", self.skill_text)
        self.assertIsNotNone(metadata_version)

        tag_version = f"v{metadata_version.group(1)}"
        for text in [self.readme_text, self.readme_en_text]:
            with self.subTest(readme=text[:20]):
                self.assertIn(f"release-{tag_version}-1f6feb", text)
                self.assertIn(f"releases/tag/{tag_version}", text)

    def test_readmes_have_language_switches(self) -> None:
        self.assertIn("语言：中文 | [English](./README_en.md)", self.readme_text)
        self.assertIn("Language: English | [中文](./README.md)", self.readme_en_text)

    def test_readmes_document_official_codex_skill_locations(self) -> None:
        required_readme_fragments = [
            "官方 Codex Agent Skills 文档",
            "https://developers.openai.com/codex/skills",
            "$CWD/.agents/skills/harmony-next",
            "$CWD/../.agents/skills/harmony-next",
            "$REPO_ROOT/.agents/skills/harmony-next",
            "$HOME/.agents/skills/harmony-next",
            "/etc/codex/skills/harmony-next",
            "可安装分发单元是 Codex plugin",
        ]
        required_readme_en_fragments = [
            "official Codex Agent Skills docs",
            "https://developers.openai.com/codex/skills",
            "$CWD/.agents/skills/harmony-next",
            "$CWD/../.agents/skills/harmony-next",
            "$REPO_ROOT/.agents/skills/harmony-next",
            "$HOME/.agents/skills/harmony-next",
            "/etc/codex/skills/harmony-next",
            "plugins are the installable distribution unit",
        ]

        for fragment in required_readme_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.readme_text)
        for fragment in required_readme_en_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.readme_en_text)

    def test_skill_documents_freshness_and_installation_paths(self) -> None:
        required_fragments = [
            "Reference snapshot:",
            "not live web docs",
            "GitHub Releases or nightly",
            "Huawei online docs",
            "Install/update entrypoints:",
            "gemini skills install",
            "Claude.ai",
            "Claude Code",
            "Codex",
            "$REPO_ROOT/.agents/skills/harmony-next",
            "$HOME/.agents/skills/harmony-next",
            "/etc/codex/skills/harmony-next",
            "package it as a Codex plugin",
        ]

        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.skill_text)

    def test_sync_release_version_updates_skill_and_readmes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            (temp_root / "harmony-next").mkdir()
            shutil.copy2(SKILL_PATH, temp_root / "harmony-next" / "SKILL.md")
            shutil.copy2(README_PATH, temp_root / "README.md")
            shutil.copy2(README_EN_PATH, temp_root / "README_en.md")

            bare_version, tag_version = sync_release_version.sync_release_version(temp_root, "v9.8.7")

            self.assertEqual(bare_version, "9.8.7")
            self.assertEqual(tag_version, "v9.8.7")
            self.assertIn('version: "9.8.7"', (temp_root / "harmony-next" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("Current local skill version: `v9.8.7`.", (temp_root / "harmony-next" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("<!-- version: 9.8.7 -->", (temp_root / "harmony-next" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("release-v9.8.7-1f6feb", (temp_root / "README.md").read_text(encoding="utf-8"))
            self.assertIn("releases/tag/v9.8.7", (temp_root / "README_en.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
