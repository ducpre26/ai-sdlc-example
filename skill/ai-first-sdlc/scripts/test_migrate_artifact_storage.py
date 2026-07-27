#!/usr/bin/env python3
"""Kiểm thử migration artifact từ tên có version sang tên file ổn định."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("migrate_artifact_storage.py")
SPEC = importlib.util.spec_from_file_location("migrate_artifact_storage", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load migrate_artifact_storage.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def artifact_text(version: str) -> str:
    """Tạo artifact Markdown tối giản với version được chỉ định."""

    return f"""---
document_id: SRS-TEST-001
document_type: srs
project: TEST
version: {version}
---
# SRS {version}
"""


class MigrationTests(unittest.TestCase):
    """Kiểm tra việc lập và áp dụng kế hoạch migration artifact."""

    def setUp(self) -> None:
        """Tạo thư mục test sạch và đăng ký bước dọn dẹp."""

        self.root = Path(__file__).with_name("_test_migration")
        if self.root.exists():
            shutil.rmtree(self.root)
        self.root.mkdir()
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_plan_selects_latest_version_and_stable_name(self) -> None:
        """Xác nhận kế hoạch chọn version mới nhất và tên ổn định."""

        (self.root / "srs.md").write_text(artifact_text("1.0.0"), encoding="utf-8")
        (self.root / "srs-v1.1.0.md").write_text(artifact_text("1.1.0"), encoding="utf-8")
        groups, errors = MODULE.discover(self.root)
        self.assertEqual(errors, [])
        items = MODULE.plan(groups)
        _, latest, candidates = items[0]
        self.assertEqual(latest.version_text, "1.1.0")
        self.assertEqual(latest.target.name, "srs.md")
        self.assertEqual(len(candidates), 2)

    def test_apply_keeps_one_live_file(self) -> None:
        """Xác nhận apply chỉ giữ một file hiện hành với nội dung mới nhất."""

        (self.root / "srs.md").write_text(artifact_text("1.0.0"), encoding="utf-8")
        (self.root / "srs-v1.1.0.md").write_text(artifact_text("1.1.0"), encoding="utf-8")
        groups, _ = MODULE.discover(self.root)
        MODULE.apply_plan(MODULE.plan(groups))
        self.assertEqual([path.name for path in self.root.glob("*.md")], ["srs.md"])
        self.assertIn("version: 1.1.0", (self.root / "srs.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
