#!/usr/bin/env python3
"""Đọc, kiểm tra và tổng hợp các file tiến độ Markdown của AI-First SDLC."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


STAGES = [
    ("initiation", "Initiation", "01-initiation"),
    ("requirements", "Requirements", "02-requirements"),
    ("design", "Design", "03-design"),
    ("development", "Development", "04-development"),
    ("testing", "Testing", "05-testing"),
    ("release", "Release", "06-release"),
    ("operations", "Operations", "07-operations"),
]
STEPS = ("inspect", "verify_inputs", "execute", "validate", "human_gate", "handoff")
STEP_STATUSES = {
    "pending", "in_progress", "awaiting_user", "awaiting_human",
    "blocked", "completed", "skipped",
}
STAGE_STATUSES = {
    "not_started", "ready", "in_progress", "awaiting_user",
    "awaiting_human", "blocked", "completed", "skipped",
}
ACTIVE_STAGE_STATUSES = {"in_progress", "awaiting_user", "awaiting_human", "blocked"}
PROPERTY_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$")
STEP_RE = re.compile(
    r"^- \[([ xX])\] `([^`]+)` — `([^`]+)`(?: — (.*))?$"
)
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} [+-]\d{2}:\d{2}$")


@dataclass
class StepProgress:
    """Biểu diễn trạng thái đã phân tích của một bước trong stage."""

    step_id: str
    checked: bool
    status: str
    note: str


@dataclass
class StageProgress:
    """Lưu checkpoint và trạng thái tổng hợp của một stage SDLC."""

    stage_id: str
    label: str
    declared_status: str
    derived_status: str
    current_step: str
    completed_steps: int
    last_updated: str
    next_action: str
    current_agent: str
    execution_id: str
    handoff_packet: str
    steps: dict[str, StepProgress]
    path: Path


def section_lines(text: str, heading: str) -> list[str]:
    """Lấy các dòng thuộc một mục Markdown cấp hai."""

    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return []
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def parse_properties(text: str) -> dict[str, str]:
    """Đọc bảng thuộc tính ở đầu file tiến độ thành từ điển."""

    properties: dict[str, str] = {}
    header = text.split("\n## Các bước", 1)[0]
    for line in header.splitlines():
        match = PROPERTY_RE.match(line)
        if not match:
            continue
        key, value = (part.strip() for part in match.groups())
        if key in {"Thuộc tính", "---"} or set(key) == {"-"}:
            continue
        properties[key] = value
    return properties


def derive_stage_status(steps: dict[str, StepProgress], declared: str) -> str:
    """Suy ra trạng thái stage từ sáu trạng thái bước và giá trị khai báo."""

    statuses = [steps[step].status for step in STEPS]
    if "blocked" in statuses:
        return "blocked"
    if "awaiting_user" in statuses:
        return "awaiting_user"
    if "awaiting_human" in statuses:
        return "awaiting_human"
    if "in_progress" in statuses:
        return "in_progress"
    if all(status == "skipped" for status in statuses):
        return "skipped"
    if all(status in {"completed", "skipped"} for status in statuses):
        return "completed"
    if all(status == "pending" for status in statuses):
        return declared if declared in {"not_started", "ready"} else "not_started"
    return "in_progress"


def parse_stage_progress(text: str, path: Path, expected_stage: str, label: str) -> StageProgress:
    """Phân tích và kiểm tra một file tiến độ stage."""

    errors: list[str] = []
    required_sections = {
        "## Các bước", "## Câu hỏi mở", "## Blocker", "## Ghi chú", "## Lịch sử",
    }
    text_lines = set(text.splitlines())
    missing_sections = sorted(required_sections - text_lines)
    if missing_sections:
        errors.append("thiếu mục: " + ", ".join(missing_sections))
    properties = parse_properties(text)
    required_properties = {
        "Stage", "Trạng thái", "Công việc", "Thao tác", "Artifact",
        "Bước hiện tại", "Cập nhật lần cuối", "Bước tiếp theo",
    }
    missing = sorted(required_properties - properties.keys())
    if missing:
        errors.append("thiếu thuộc tính: " + ", ".join(missing))

    declared_stage = properties.get("Stage", "")
    if declared_stage != expected_stage:
        errors.append(f"Stage phải là {expected_stage}, nhận {declared_stage or 'trống'}")

    declared_status = properties.get("Trạng thái", "")
    if declared_status not in STAGE_STATUSES:
        errors.append(f"trạng thái stage không hợp lệ: {declared_status or 'trống'}")

    last_updated = properties.get("Cập nhật lần cuối", "—")
    if last_updated not in {"—", "-"} and not TIMESTAMP_RE.fullmatch(last_updated):
        errors.append(f"thời gian không hợp lệ: {last_updated}")

    steps: dict[str, StepProgress] = {}
    for line in section_lines(text, "## Các bước"):
        match = STEP_RE.match(line.strip())
        if not match:
            continue
        mark, step_id, status, note = match.groups()
        if step_id in steps:
            errors.append(f"bước bị lặp: {step_id}")
            continue
        if step_id not in STEPS:
            errors.append(f"bước không hợp lệ: {step_id}")
        if status not in STEP_STATUSES:
            errors.append(f"trạng thái bước không hợp lệ: {step_id}={status}")
        checked = mark.lower() == "x"
        should_be_checked = status in {"completed", "skipped"}
        if checked != should_be_checked:
            errors.append(f"checkbox không khớp trạng thái: {step_id}={status}")
        steps[step_id] = StepProgress(step_id, checked, status, note or "")

    missing_steps = [step for step in STEPS if step not in steps]
    if missing_steps:
        errors.append("thiếu bước: " + ", ".join(missing_steps))

    if errors:
        raise ValueError("; ".join(errors))

    derived = derive_stage_status(steps, declared_status)
    if declared_status != derived:
        raise ValueError(f"trạng thái stage {declared_status} không khớp checklist; phải là {derived}")
    if derived == "skipped":
        notes = [line.strip() for line in section_lines(text, "## Ghi chú") if line.strip()]
        if not notes or all(line == "Không có." for line in notes):
            raise ValueError("stage skipped phải ghi lý do trong mục Ghi chú")

    active_steps = [step.step_id for step in steps.values() if step.status in {
        "in_progress", "awaiting_user", "awaiting_human", "blocked",
    }]
    if len(active_steps) > 1:
        raise ValueError(
            "chỉ được có một bước hoạt động, nhận: " + ", ".join(active_steps)
        )
    declared_current = properties.get("Bước hiện tại", "—")
    if active_steps and declared_current != active_steps[0]:
        raise ValueError(f"Bước hiện tại phải là {active_steps[0]}, nhận {declared_current}")
    if not active_steps and declared_current not in {"—", "-"}:
        raise ValueError("Bước hiện tại phải là — khi không có bước hoạt động")

    return StageProgress(
        stage_id=expected_stage,
        label=label,
        declared_status=declared_status,
        derived_status=derived,
        current_step=declared_current,
        completed_steps=sum(1 for step in steps.values() if step.checked),
        last_updated=last_updated,
        next_action=properties.get("Bước tiếp theo", "—"),
        current_agent=properties.get("Agent hiện tại", "—"),
        execution_id=properties.get("Execution ID", "—"),
        handoff_packet=properties.get("Handoff packet", "—"),
        steps=steps,
        path=path,
    )


def derive_overall_status(records: list[StageProgress], missing_count: int = 0) -> str:
    """Tính trạng thái toàn dự án từ các stage đã đọc và số stage bị thiếu."""

    statuses = [record.derived_status for record in records]
    if any(status in {"blocked", "awaiting_user"} for status in statuses):
        return "attention_required"
    if "awaiting_human" in statuses:
        return "awaiting_human"
    if not missing_count and len(records) == len(STAGES) and all(
        status in {"completed", "skipped"} for status in statuses
    ):
        return "completed"
    if any(status in {"ready", "in_progress", "completed", "skipped"} for status in statuses):
        return "in_progress"
    return "not_started"


def read_project_name(root_progress: Path) -> str:
    """Đọc tên dự án từ file tiến độ tổng, dùng giá trị mặc định khi thiếu."""

    if not root_progress.exists():
        return "CHƯA-XÁC-ĐỊNH"
    for line in root_progress.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("- Dự án:"):
            return line.split(":", 1)[1].strip() or "CHƯA-XÁC-ĐỊNH"
    return "CHƯA-XÁC-ĐỊNH"


def inspect_progress(docs_root: Path) -> tuple[list[StageProgress], list[str]]:
    """Kiểm tra tiến độ của bảy stage và trả về bản ghi cùng danh sách lỗi."""

    records: list[StageProgress] = []
    issues: list[str] = []
    for stage_id, label, directory in STAGES:
        path = docs_root / directory / "_progress.md"
        if not path.exists():
            issues.append(f"{label}: progress_missing ({path})")
            continue
        try:
            records.append(parse_stage_progress(
                path.read_text(encoding="utf-8-sig"), path, stage_id, label
            ))
        except (OSError, UnicodeError, ValueError) as exc:
            issues.append(f"{label}: {exc}")
    return records, issues


def render_summary(project: str, records: list[StageProgress], issues: list[str]) -> str:
    """Tạo báo cáo Markdown tóm tắt tiến độ và các vấn đề cần chú ý."""

    overall = derive_overall_status(records, len(STAGES) - len(records))
    active = [record.label for record in records if record.derived_status in ACTIVE_STAGE_STATUSES]
    lines = [
        "# Kiểm tra tiến độ AI-First SDLC",
        "",
        f"- Dự án: {project}",
        f"- Trạng thái tổng thể: {overall}",
        f"- Stage đang hoạt động: {', '.join(active) if active else '—'}",
        "",
        "## Tổng hợp stage",
        "",
        "| Stage | Trạng thái | Bước hiện tại | Agent | Hoàn thành | Cập nhật lần cuối |",
        "|---|---|---|---|---:|---|",
    ]
    by_stage = {record.stage_id: record for record in records}
    for stage_id, label, _ in STAGES:
        record = by_stage.get(stage_id)
        if record:
            lines.append(
                f"| {label} | {record.derived_status} | {record.current_step} | {record.current_agent} | "
                f"{record.completed_steps}/6 | {record.last_updated} |"
            )
        else:
            lines.append(f"| {label} | progress_missing | — | — | 0/6 | — |")
    lines.extend(["", "## Công việc cần chú ý", ""])
    attention = [record for record in records if record.derived_status in {
        "blocked", "awaiting_user", "awaiting_human",
    }]
    if attention:
        lines.extend(
            f"- {record.label}: {record.derived_status}; bước {record.current_step}; "
            f"tiếp theo: {record.next_action}." for record in attention
        )
    else:
        lines.append("Không có.")
    if issues:
        lines.extend(["", "## Lỗi progress", ""])
        lines.extend(f"- {issue}" for issue in issues)
    return "\n".join(lines) + "\n"


def main() -> int:
    """Chạy lệnh kiểm tra tiến độ và trả mã thoát phù hợp."""

    if len(sys.argv) != 2:
        print("Usage: python inspect_progress.py <docs/ai-sdlc>")
        return 2
    docs_root = Path(sys.argv[1])
    if not docs_root.is_dir():
        print(f"ERROR: progress root not found: {docs_root}")
        return 2
    records, issues = inspect_progress(docs_root)
    print(render_summary(read_project_name(docs_root / "_progress.md"), records, issues), end="")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
