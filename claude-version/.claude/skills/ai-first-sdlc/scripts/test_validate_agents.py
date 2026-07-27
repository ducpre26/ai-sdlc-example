#!/usr/bin/env python3
"""Kiểm thử validator cho bản Claude Code của bộ AI-first SDLC."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_agents.py")
SPEC = importlib.util.spec_from_file_location("validate_agents", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load validate_agents.py")
validate_agents = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_agents
SPEC.loader.exec_module(validate_agents)


class ValidateClaudeAgentsTests(unittest.TestCase):
    """Kiểm tra discovery, preload và separation of duties."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_root = Path(__file__).resolve().parents[1]
        cls.project_root = Path(__file__).resolve().parents[4]

    def setUp(self) -> None:
        self.work_root = Path(__file__).with_name("_test_claude_agents")
        shutil.rmtree(self.work_root, ignore_errors=True)
        self.work_root.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.work_root, ignore_errors=True)

    def test_distribution_is_valid(self) -> None:
        """Bản phân phối Claude phải đạt toàn bộ contract."""

        errors = validate_agents.validate(
            self.skill_root,
            project_root=self.project_root,
        )
        self.assertEqual(errors, [])

    def test_agent_requires_name_and_description(self) -> None:
        """Agent thiếu trường native bắt buộc phải bị từ chối."""

        path = self.work_root / "broken.md"
        path.write_text("---\nname: broken\n---\nPrompt\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "description"):
            validate_agents.parse_agent(path)

    def test_missing_preloaded_skill_is_reported(self) -> None:
        """Agent chuyên môn phải preload đúng companion skill."""

        source = self.project_root / ".claude" / "agents"
        for path in source.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            if path.name == "development-agent.md":
                text = text.replace("  - sdlc-software-development\n", "")
            (self.work_root / path.name).write_text(text, encoding="utf-8")
        _, errors = validate_agents.load_agents(self.work_root)
        self.assertTrue(any("development-agent.md: skills must preload" in item for item in errors))

    def test_shared_executor_and_reviewer_binding_is_rejected(self) -> None:
        """Executor và reviewer không được dùng chung target."""

        config = self.work_root / "config.yaml"
        config.write_text(
            "agent_bindings:\n"
            "  qa-agent:\n"
            "    target: shared-agent\n"
            "  qa-review-agent:\n"
            "    target: shared-agent\n",
            encoding="utf-8",
        )
        errors = validate_agents.validate(
            self.skill_root,
            config_path=config,
            project_root=self.project_root,
        )
        self.assertTrue(any("strict separation violated" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
