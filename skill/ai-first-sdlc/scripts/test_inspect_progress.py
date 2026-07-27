#!/usr/bin/env python3
"""Kiểm thử hồi quy cho việc đọc và tổng hợp tiến độ SDLC bằng Markdown."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("inspect_progress.py")
SPEC = importlib.util.spec_from_file_location("inspect_progress", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load inspect_progress.py")
PROGRESS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PROGRESS
SPEC.loader.exec_module(PROGRESS)


def progress_text(
    stage: str = "requirements",
    stage_status: str = "in_progress",
    current_step: str = "execute",
    step_statuses: dict[str, str] | None = None,
) -> str:
    """Tạo nội dung progress hợp lệ hoặc tùy biến để dùng trong test."""

    statuses = step_statuses or {
        "inspect": "completed",
        "verify_inputs": "completed",
        "execute": "in_progress",
        "validate": "pending",
        "human_gate": "pending",
        "handoff": "pending",
    }
    step_lines = []
    for step in PROGRESS.STEPS:
        status = statuses[step]
        mark = "x" if status in {"completed", "skipped"} else " "
        step_lines.append(f"- [{mark}] `{step}` — `{status}`")
    return f"""# Tiến độ — Requirements

| Thuộc tính | Giá trị |
|---|---|
| Stage | {stage} |
| Trạng thái | {stage_status} |
| Công việc | Cập nhật SRS |
| Thao tác | update |
| Artifact | SRS-TEST-001@1.1.0 |
| Agent hiện tại | qa-agent |
| Execution ID | qa-run-001 |
| Handoff packet | docs/ai-sdlc/02-requirements/_handoff.md |
| Bước hiện tại | {current_step} |
| Cập nhật lần cuối | 2026-07-22 15:30 +07:00 |
| Bước tiếp theo | Hoàn thiện acceptance criteria |

## Các bước

{chr(10).join(step_lines)}

## Câu hỏi mở

Không có.

## Blocker

Không có.

## Ghi chú

Đang xử lý theo kế hoạch.

## Lịch sử

| Thời gian | Bước | Trạng thái | Nội dung |
|---|---|---|---|
| 2026-07-22 15:30 +07:00 | execute | in_progress | Bắt đầu xử lý |
"""


class ProgressInspectionTests(unittest.TestCase):
    """Kiểm tra quy tắc trạng thái, checkbox và báo cáo tiến độ."""

    def parse(self, text: str):
        """Phân tích progress mẫu của stage Requirements."""

        return PROGRESS.parse_stage_progress(
            text, Path("02-requirements/_progress.md"), "requirements", "Requirements"
        )

    def test_completed_checkbox_is_counted(self) -> None:
        """Xác nhận checkbox hoàn thành được tính và giữ thông tin agent."""

        record = self.parse(progress_text())
        self.assertEqual(record.completed_steps, 2)
        self.assertEqual(record.current_step, "execute")
        self.assertEqual(record.current_agent, "qa-agent")

    def test_awaiting_user_has_priority(self) -> None:
        """Xác nhận awaiting_user được ưu tiên khi suy ra trạng thái stage."""

        statuses = {
            "inspect": "completed",
            "verify_inputs": "completed",
            "execute": "awaiting_user",
            "validate": "pending",
            "human_gate": "pending",
            "handoff": "pending",
        }
        record = self.parse(progress_text("requirements", "awaiting_user", "execute", statuses))
        self.assertEqual(record.derived_status, "awaiting_user")

    def test_checkbox_must_match_status(self) -> None:
        """Từ chối checkbox không khớp trạng thái của bước."""

        text = progress_text().replace("- [x] `inspect` — `completed`", "- [ ] `inspect` — `completed`")
        with self.assertRaisesRegex(ValueError, "checkbox không khớp"):
            self.parse(text)

    def test_all_steps_complete_the_stage(self) -> None:
        """Xác nhận sáu bước hoàn thành làm stage hoàn thành."""

        statuses = {step: "completed" for step in PROGRESS.STEPS}
        record = self.parse(progress_text("requirements", "completed", "—", statuses))
        self.assertEqual(record.derived_status, "completed")
        self.assertEqual(record.completed_steps, 6)

    def test_overall_attention_required(self) -> None:
        """Xác nhận stage bị chặn làm toàn dự án cần chú ý."""

        statuses = {
            "inspect": "completed",
            "verify_inputs": "completed",
            "execute": "blocked",
            "validate": "pending",
            "human_gate": "pending",
            "handoff": "pending",
        }
        record = self.parse(progress_text("requirements", "blocked", "execute", statuses))
        self.assertEqual(PROGRESS.derive_overall_status([record], 6), "attention_required")

    def test_multiple_active_steps_are_invalid(self) -> None:
        """Từ chối stage có nhiều hơn một bước đang hoạt động."""

        statuses = {
            "inspect": "completed",
            "verify_inputs": "completed",
            "execute": "in_progress",
            "validate": "awaiting_user",
            "human_gate": "pending",
            "handoff": "pending",
        }
        with self.assertRaisesRegex(ValueError, "một bước hoạt động"):
            self.parse(progress_text("requirements", "awaiting_user", "execute", statuses))

    def test_all_seven_completed_means_overall_completed(self) -> None:
        """Xác nhận bảy stage hoàn thành làm toàn dự án hoàn thành."""

        statuses = {step: "completed" for step in PROGRESS.STEPS}
        record = self.parse(progress_text("requirements", "completed", "—", statuses))
        self.assertEqual(
            PROGRESS.derive_overall_status([record] * 7, 0),
            "completed",
        )

    def test_summary_reports_counts_and_missing_progress(self) -> None:
        """Xác nhận báo cáo hiển thị số bước và stage thiếu progress."""

        record = self.parse(progress_text())
        summary = PROGRESS.render_summary(
            "TASKFLOW",
            [record],
            ["Design: progress_missing"],
        )
        self.assertIn("| Requirements | in_progress | execute | qa-agent | 2/6 |", summary)
        self.assertIn("| Design | progress_missing | — | — | 0/6 | — |", summary)
        self.assertIn("- Design: progress_missing", summary)

    def test_missing_required_section_is_invalid(self) -> None:
        """Từ chối file progress thiếu mục bắt buộc."""

        text = progress_text().replace("## Blocker\n\nKhông có.\n\n", "")
        with self.assertRaisesRegex(ValueError, "thiếu mục: ## Blocker"):
            self.parse(text)

    def test_skipped_stage_requires_reason(self) -> None:
        """Yêu cầu lý do khi toàn bộ stage được đánh dấu skipped."""

        statuses = {step: "skipped" for step in PROGRESS.STEPS}
        text = progress_text("requirements", "skipped", "—", statuses).replace(
            "Đang xử lý theo kế hoạch.",
            "Không có.",
        )
        with self.assertRaisesRegex(ValueError, "phải ghi lý do"):
            self.parse(text)


if __name__ == "__main__":
    unittest.main()
