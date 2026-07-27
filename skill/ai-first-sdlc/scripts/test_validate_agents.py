#!/usr/bin/env python3
"""Kiểm thử custom agent Codex, workflow SDLC và separation of duties."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_agents.py")
SPEC = importlib.util.spec_from_file_location("validate_agents", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load validate_agents.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def find_project_root(skill_root: Path) -> Path:
    """Tìm project root cho cả layout nguồn và layout skill cài theo dự án."""

    for candidate in (skill_root, *skill_root.parents):
        if (candidate / ".codex" / "agents").is_dir():
            return candidate
    raise RuntimeError(f"cannot find project root from {skill_root}")


class AgentWorkflowTests(unittest.TestCase):
    """Kiểm tra cấu trúc và các ràng buộc điều phối agent của repository."""

    def setUp(self) -> None:
        """Xác định skill root và project root dùng cho từng test."""

        self.skill_root = Path(__file__).resolve().parents[1]
        self.project_root = find_project_root(self.skill_root)

    def test_repository_agent_contract_is_valid(self) -> None:
        """Xác nhận contract agent hiện tại của repository không có lỗi."""

        self.assertEqual(MODULE.validate(self.skill_root, project_root=self.project_root), [])

    def test_strict_separation_rejects_shared_target(self) -> None:
        """Từ chối executor và reviewer dùng chung một target."""

        config = Path(__file__).with_name("_test_agent_config.yaml")
        self.addCleanup(config.unlink, missing_ok=True)
        config.write_text(
            "agent_bindings:\n"
            "  qa-agent:\n    target: shared-agent\n"
            "  qa-review-agent:\n    target: shared-agent\n",
            encoding="utf-8",
        )
        errors = MODULE.validate(self.skill_root, config, self.project_root)
        self.assertTrue(any("strict separation violated" in error for error in errors))

    def test_human_gate_cannot_be_delegated(self) -> None:
        """Xác nhận mọi human gate luôn được ánh xạ tới con người."""

        workflow = MODULE.parse_workflow(self.skill_root / "references" / "agent-workflow.yaml")
        self.assertTrue(all(mapping["human_gate"].agent == "human" for mapping in workflow.values()))
        self.assertTrue(all(not mapping["human_gate"].required_skills for mapping in workflow.values()))

    def test_companion_skill_contract_is_valid(self) -> None:
        """Xác nhận đủ mười companion skill với frontmatter chuẩn."""

        self.assertEqual(MODULE.validate_companion_skills(self.skill_root.parent), [])
        self.assertEqual(
            {path.name for path in self.skill_root.parent.glob("sdlc-*") if path.is_dir()},
            MODULE.EXPECTED_SKILLS,
        )

    def test_stage_references_only_keep_stage_contract(self) -> None:
        """Xác nhận bảy reference không còn chứa hướng dẫn nghiệp vụ chi tiết."""

        self.assertEqual(MODULE.validate_stage_contracts(self.skill_root), [])

    def test_guided_discovery_lives_inside_agent_skills(self) -> None:
        """Xác nhận nội dung discovery nằm trực tiếp trong hai companion skill."""

        for skill_name, sections in MODULE.REQUIRED_DISCOVERY_SECTIONS.items():
            skill_root = self.skill_root.parent / skill_name
            text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            self.assertFalse((skill_root / "references").exists())
            for section in sections:
                self.assertIn(section, text)

    def test_all_companion_skills_keep_migrated_stage_context(self) -> None:
        """Xác nhận context nghiệp vụ trọng yếu đã chuyển đủ vào từng skill."""

        self.assertEqual(set(MODULE.REQUIRED_CONTEXT_MARKERS), MODULE.EXPECTED_SKILLS)
        for skill_name, markers in MODULE.REQUIRED_CONTEXT_MARKERS.items():
            text = (self.skill_root.parent / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, text)

    def test_executor_and_reviewer_use_distinct_skills(self) -> None:
        """Xác nhận các bước cần độc lập không dùng chung companion skill."""

        workflow = MODULE.parse_workflow(self.skill_root / "references" / "agent-workflow.yaml")
        for stage in ("requirements", "development", "testing"):
            self.assertNotEqual(
                workflow[stage]["execute"].required_skills,
                workflow[stage]["validate"].required_skills,
            )

    def test_inspect_handoff_and_human_gate_do_not_require_domain_skill(self) -> None:
        """Xác nhận chỉ bước nghiệp vụ mới nạp companion skill."""

        workflow = MODULE.parse_workflow(self.skill_root / "references" / "agent-workflow.yaml")
        for mapping in workflow.values():
            for step in ("inspect", "human_gate", "handoff"):
                self.assertEqual(mapping[step].required_skills, [])

    def test_definitions_use_native_codex_toml_schema(self) -> None:
        """Xác nhận năm agent dùng các trường TOML native bắt buộc."""

        agents, errors = MODULE.load_agents(self.project_root / ".codex" / "agents")
        self.assertEqual(errors, [])
        self.assertEqual(set(agents), MODULE.EXPECTED_AGENTS)
        for definition in agents.values():
            self.assertTrue(MODULE.REQUIRED_AGENT_FIELDS <= definition.config.keys())

    def test_markdown_agent_definitions_are_not_used(self) -> None:
        """Xác nhận không còn dùng Markdown làm custom agent definition."""

        self.assertEqual(list((self.skill_root / "agents" / "definitions").glob("*.md")), [])

    def test_skill_agents_directory_only_contains_openai_metadata(self) -> None:
        """Xác nhận thư mục agents của skill chỉ chứa metadata openai.yaml."""

        files = sorted(path.name for path in (self.skill_root / "agents").iterdir() if path.is_file())
        self.assertEqual(files, ["openai.yaml"])

    def test_project_validation_detects_missing_native_agents(self) -> None:
        """Xác nhận validator phát hiện dự án chưa cài custom agent."""

        project_root = self.skill_root / "scripts" / "_missing_agent_project"
        self.assertFalse(project_root.exists())
        errors = MODULE.validate(self.skill_root, project_root=project_root)
        self.assertTrue(any("native Codex agent directory not found" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
