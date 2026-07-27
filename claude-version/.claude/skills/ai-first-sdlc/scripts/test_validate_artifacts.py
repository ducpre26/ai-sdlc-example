#!/usr/bin/env python3
"""Kiểm thử hồi quy cho artifact validator của AI-First SDLC."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import shutil
import stat
import sys
import time
import unittest
from pathlib import Path


VALIDATOR_PATH = Path(__file__).with_name("validate_artifacts.py")
SPEC = importlib.util.spec_from_file_location("validate_artifacts", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load validate_artifacts.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def remove_tree(path: Path) -> None:
    """Xóa cây thư mục test, kể cả file bị đánh dấu chỉ đọc trên Windows."""

    if not path.exists():
        return
    def clear_readonly(function, target, _error):
        """Gỡ cờ chỉ đọc rồi thử lại thao tác dọn dẹp bị lỗi."""

        os.chmod(target, stat.S_IWRITE)
        function(target)
    for attempt in range(10):
        try:
            shutil.rmtree(path, onexc=clear_readonly)
            return
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(0.05)


def artifact(
    name: str,
    document_id: str,
    version: str,
    status: str,
    previous_status: str | None,
    supersedes_version: str | None = None,
    source_documents: list[str] | None = None,
):
    """Tạo đối tượng artifact tối giản phục vụ kiểm thử version và lifecycle."""

    checked_at = "2026-07-22" if status != "draft" else None
    approved = status in {"approved", "superseded"}
    metadata = {
        "document_id": document_id,
        "document_type": "srs",
        "project": "TEST",
        "version": version,
        "supersedes_version": supersedes_version,
        "status": status,
        "previous_status": previous_status,
        "owner": "Product Owner",
        "approver": "Business Owner",
        "created_at": "2026-07-22",
        "updated_at": "2026-07-22",
        "source_documents": source_documents or [],
        "related_documents": [],
        "related_work_items": [],
        "evidence": [],
        "open_questions": [],
        "ai_generated": True,
        "ai_checked_at": checked_at,
        "human_decision": "approved" if approved else None,
        "human_approved_at": "2026-07-22" if approved else None,
    }
    return VALIDATOR.Artifact(path=Path(name), metadata=metadata, body="# Test artifact")


class ValidatorVersioningTests(unittest.TestCase):
    """Kiểm tra quy tắc version, lịch sử Git và file hiện hành duy nhất."""

    def messages(self, artifacts: list, historical_versions=None) -> list[str]:
        """Chạy validation và chỉ trả về nội dung lỗi."""

        errors, _ = VALIDATOR.validate_collection(artifacts, historical_versions)
        return [message for _, message in errors]

    def test_only_one_live_file_per_document_id(self) -> None:
        """Từ chối nhiều file hiện hành dùng chung document ID."""

        messages = self.messages([
            artifact("v1.md", "SRS-TEST-001", "1.0.0", "approved", "human_review"),
            artifact("v2.md", "SRS-TEST-001", "1.1.0", "draft", None, "1.0.0"),
        ], {("SRS-TEST-001", "1.0.0")})
        self.assertTrue(any("multiple live files" in message for message in messages))

    def test_exact_document_version_must_be_unique(self) -> None:
        """Từ chối document ID và version bị trùng hoàn toàn."""

        messages = self.messages([
            artifact("a.md", "SRS-TEST-001", "1.0.0", "draft", None),
            artifact("b.md", "SRS-TEST-001", "1.0.0", "draft", None),
        ])
        self.assertTrue(any("duplicate document_id and version" in message for message in messages))

    def test_supersedes_version_must_be_lower(self) -> None:
        """Từ chối supersedes_version không thấp hơn version hiện tại."""

        messages = self.messages([
            artifact("artifact.md", "SRS-TEST-001", "1.0.0", "draft", None, "1.0.0"),
        ])
        self.assertTrue(any("supersedes_version must be lower" in message for message in messages))

    def test_versioned_document_reference_resolves(self) -> None:
        """Chấp nhận tham chiếu document ID kèm version đang tồn tại."""

        messages = self.messages([
            artifact("source.md", "SRS-TEST-001", "1.0.0", "approved", "human_review"),
            artifact(
                "target.md",
                "SRS-TEST-002",
                "1.0.0",
                "draft",
                None,
                source_documents=["SRS-TEST-001@1.0.0"],
            ),
        ])
        self.assertEqual(messages, [])

    def test_historical_reference_resolves_without_live_snapshot(self) -> None:
        """Chấp nhận tham chiếu chỉ còn tồn tại trong lịch sử Git."""

        target = artifact(
            "target.md", "SRS-TEST-002", "1.0.0", "draft", None,
            source_documents=["SRS-TEST-001@1.0.0"],
        )
        messages = self.messages([target], {("SRS-TEST-001", "1.0.0")})
        self.assertEqual(messages, [])

    def test_supersedes_version_resolves_from_history(self) -> None:
        """Chấp nhận version bị thay thế khi version đó có trong lịch sử."""

        current = artifact("srs.md", "SRS-TEST-001", "1.1.0", "draft", None, "1.0.0")
        self.assertEqual(self.messages([current], {("SRS-TEST-001", "1.0.0")}), [])

    def test_versioned_filename_is_rejected(self) -> None:
        """Từ chối tên file artifact chứa hậu tố semantic version."""

        messages = self.messages([artifact("srs-v1.0.0.md", "SRS-TEST-001", "1.0.0", "draft", None)])
        self.assertTrue(any("versioned filename is legacy" in message for message in messages))

    def test_multiline_frontmatter_array_is_supported(self) -> None:
        """Xác nhận parser hỗ trợ danh sách frontmatter nhiều dòng."""

        text = """---
document_id: SRS-TEST-001
version: 1.0.0
source_documents:
  - PC-TEST-001@1.0.0
---
# Body
"""
        parsed = VALIDATOR.parse_artifact_text(text, Path("srs.md"))
        self.assertEqual(parsed.metadata["source_documents"], ["PC-TEST-001@1.0.0"])

    def test_git_history_indexes_old_stable_version(self) -> None:
        """Xác nhận validator lập chỉ mục version cũ từ Git history."""

        root = Path(__file__).with_name("_test_git_repo")
        remove_tree(root)
        root.mkdir()
        self.addCleanup(remove_tree, root)
        docs = root / "docs" / "ai-sdlc"
        docs.mkdir(parents=True)
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        source = docs / "srs.md"
        source.write_text("---\ndocument_id: SRS-TEST-001\nversion: 1.0.0\n---\n# SRS\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "baseline"], cwd=root, check=True, capture_output=True)
        versions = VALIDATOR.git_history_versions(root, docs)
        self.assertIn(("SRS-TEST-001", "1.0.0"), versions)
        self.assertTrue(VALIDATOR.artifact_is_committed(root, source))

    def test_progress_markdown_is_not_an_artifact(self) -> None:
        """Xác nhận file progress không bị phân loại thành artifact."""

        self.assertFalse(VALIDATOR.is_artifact_markdown(Path("_progress.md")))
        self.assertTrue(VALIDATOR.is_artifact_markdown(Path("srs.md")))


if __name__ == "__main__":
    unittest.main()
