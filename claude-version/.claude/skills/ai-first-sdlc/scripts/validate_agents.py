#!/usr/bin/env python3
"""Kiểm tra custom agent, companion skill, workflow SDLC và agent binding."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


STAGES = ("initiation", "requirements", "design", "development", "testing", "release", "operations")
STEPS = ("inspect", "verify_inputs", "execute", "validate", "human_gate", "handoff")
REQUIRED_AGENT_FIELDS = {"name", "description"}
EXPECTED_AGENTS = {
    "sdlc-orchestrator-agent",
    "qa-agent",
    "qa-review-agent",
    "development-agent",
    "code-review-agent",
}
EXPECTED_SKILLS = {
    "sdlc-project-initiation",
    "sdlc-requirements-engineering",
    "sdlc-requirements-review",
    "sdlc-solution-design",
    "sdlc-software-development",
    "sdlc-code-review",
    "sdlc-software-testing",
    "sdlc-test-review",
    "sdlc-release-management",
    "sdlc-service-operations",
}
EXPECTED_AGENT_SKILLS = {
    "sdlc-orchestrator-agent": {"ai-first-sdlc"},
    "qa-agent": {"sdlc-requirements-engineering", "sdlc-software-testing"},
    "qa-review-agent": {"sdlc-requirements-review", "sdlc-test-review"},
    "development-agent": {"sdlc-software-development"},
    "code-review-agent": {"sdlc-code-review"},
}
EXPECTED_ASSIGNMENTS = {
    ("requirements", "verify_inputs"): ("qa-agent", ["sdlc-requirements-engineering"]),
    ("requirements", "execute"): ("qa-agent", ["sdlc-requirements-engineering"]),
    ("requirements", "validate"): ("qa-review-agent", ["sdlc-requirements-review"]),
    ("development", "verify_inputs"): ("development-agent", ["sdlc-software-development"]),
    ("development", "execute"): ("development-agent", ["sdlc-software-development"]),
    ("development", "validate"): ("code-review-agent", ["sdlc-code-review"]),
    ("testing", "verify_inputs"): ("qa-agent", ["sdlc-software-testing"]),
    ("testing", "execute"): ("qa-agent", ["sdlc-software-testing"]),
    ("testing", "validate"): ("qa-review-agent", ["sdlc-test-review"]),
}
REQUIRED_DISCOVERY_SECTIONS = {
    "sdlc-project-initiation": (
        "## Guided discovery cho Initiation",
        "### Chu kỳ đặt câu hỏi",
        "### Cách ghi nhận câu trả lời",
        "### Chọn kỹ thuật khám phá",
        "### Nhóm câu hỏi: vấn đề và giá trị",
        "### Nhóm câu hỏi: stakeholder và thẩm quyền",
        "### Nhóm câu hỏi: mục tiêu và đo lường",
        "### Nhóm câu hỏi: phạm vi, ràng buộc và rủi ro",
        "### Kết thúc một vòng discovery",
    ),
    "sdlc-requirements-engineering": (
        "## Guided discovery và elicitation",
        "### Chu kỳ đặt câu hỏi",
        "### Cách ghi nhận câu trả lời",
        "### Chọn kỹ thuật elicitation",
        "### Nhóm câu hỏi: kế hoạch elicitation và hiện trạng",
        "### Nhóm câu hỏi: hành vi chức năng và quy tắc",
        "### Nhóm câu hỏi: dữ liệu, tích hợp và chuyển đổi",
        "### Nhóm câu hỏi: NFR và trải nghiệm",
        "### Nhóm câu hỏi: ưu tiên và truy vết",
        "### Kết thúc một vòng elicitation",
    ),
}
REQUIRED_CONTEXT_MARKERS = {
    "sdlc-project-initiation": (
        "Ưu tiên lý do kinh doanh",
        "Tailor mức gọn nhẹ",
        "consent, nơi lưu, quyền truy cập và retention",
        "không làm, mua sản phẩm hoặc đổi quy trình",
        "supersedes_version",
        "Go/Conditional Go/No-Go",
    ),
    "sdlc-requirements-engineering": (
        "trung lập về giải pháp",
        "candidate_requirement",
        "Must, Should, Could hoặc Won't",
        "Load, concurrency, data volume và growth rate",
        "supersedes_version",
        "số tổng hợp khớp chi tiết",
    ),
    "sdlc-requirements-review": (
        "solution bias",
        "numeric target",
        "Security/data/interface/privacy/audit/error behavior",
        "summary count khớp chi tiết",
    ),
    "sdlc-solution-design": (
        "trust boundary",
        "retry, idempotency, transaction, concurrency",
        "supersedes_version",
        "OpenAPI liên kết `API-###`",
    ),
    "sdlc-software-development": (
        "feature flag",
        "Definition of Done",
        "supersedes_version",
        "file/component thay đổi",
    ),
    "sdlc-code-review": (
        "transaction, concurrency",
        "migration, rollout order, feature flag và rollback",
        "`skipped`, `flaky`, `failed` hoặc `not_run`",
        "Known limitation",
    ),
    "sdlc-software-testing": (
        "retry/idempotency",
        "residual risk",
        "supersedes_version",
        "UAT dùng business scenario",
    ),
    "sdlc-test-review": (
        "`skipped`, `flaky`, `blocked`, `not_run`",
        "NFR metric, target, measurement condition",
        "UAT liên kết business scenario",
        "summary count khớp",
    ),
    "sdlc-release-management": (
        "build bất biến",
        "observation window",
        "supersedes_version",
        "Breaking change",
    ),
    "sdlc-service-operations": (
        "Postmortem blameless",
        "SLI/SLO/SLA",
        "failover/failback",
        "supersedes_version",
        "cost of delay",
    ),
}
STAGE_CONTRACT_HEADINGS = (
    "## 1. Mục đích và phạm vi",
    "## 2. Điều kiện kích hoạt",
    "## 3. Artifact đầu vào",
    "## 4. Artifact đầu ra",
    "## 5. Nguồn và evidence bắt buộc",
    "## 6. Ánh xạ step, agent và skill",
    "## 7. Traceability contract",
    "## 8. Điều kiện chặn",
    "## 9. Human gate",
    "## 10. Handoff contract",
    "## 11. Ngoại lệ",
)


@dataclass
class AgentDefinition:
    """Lưu đường dẫn và frontmatter Markdown của một Claude Code subagent."""

    path: Path
    config: dict[str, object]


@dataclass
class WorkflowStep:
    """Lưu agent và companion skill bắt buộc của một stage step."""

    agent: str
    required_skills: list[str]


def parse_frontmatter(path: Path) -> dict[str, object]:
    """Đọc subset YAML frontmatter dùng bởi skill và Claude Code subagent."""

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("unclosed YAML frontmatter") from exc

    config: dict[str, object] = {}
    current_list: str | None = None
    current_scalar: str | None = None
    for number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list:
            value = line[4:].strip().strip("'\"")
            assert isinstance(config[current_list], list)
            config[current_list].append(value)
            continue
        if line[0].isspace() and current_scalar:
            previous = str(config[current_scalar])
            config[current_scalar] = f"{previous} {line.strip()}".strip()
            continue
        if line[0].isspace() or ":" not in line:
            raise ValueError(f"unsupported frontmatter structure at line {number}")
        key, value = (part.strip() for part in line.split(":", 1))
        if not value:
            config[key] = []
            current_list = key
            current_scalar = None
        elif value in {">", ">-", "|", "|-"}:
            config[key] = ""
            current_list = None
            current_scalar = key
        else:
            config[key] = value.strip("'\"")
            current_list = None
            current_scalar = None
    return config


def parse_agent(path: Path) -> dict[str, object]:
    """Đọc Markdown và kiểm tra frontmatter bắt buộc của Claude Code."""

    config = parse_frontmatter(path)
    missing = sorted(REQUIRED_AGENT_FIELDS - config.keys())
    if missing:
        raise ValueError("missing required Claude Code fields: " + ", ".join(missing))
    for field in REQUIRED_AGENT_FIELDS:
        if not isinstance(config[field], str) or not config[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    return config


def load_agents(directory: Path) -> tuple[dict[str, AgentDefinition], list[str]]:
    """Nạp năm Claude Code subagent từ thư mục và thu thập lỗi cấu trúc."""

    agents: dict[str, AgentDefinition] = {}
    errors: list[str] = []
    if not directory.is_dir():
        return agents, [f"{directory}: Claude Code agent directory not found"]
    for path in sorted(directory.glob("*.md")):
        try:
            config = parse_agent(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        name = str(config["name"])
        if path.stem != name:
            errors.append(f"{path}: filename must match agent name {name}")
        if name in agents:
            errors.append(f"{path}: duplicate agent name: {name}")
        agents[name] = AgentDefinition(path, config)
    missing = sorted(EXPECTED_AGENTS - agents.keys())
    if missing:
        errors.append("missing Claude Code agents: " + ", ".join(missing))
    for name in sorted(EXPECTED_AGENTS & agents.keys()):
        declared = agents[name].config.get("skills", [])
        if not isinstance(declared, list):
            errors.append(f"{agents[name].path}: skills must be a YAML list")
            continue
        expected = EXPECTED_AGENT_SKILLS[name]
        if set(str(item) for item in declared) != expected:
            errors.append(
                f"{agents[name].path}: skills must preload " + ", ".join(sorted(expected))
            )
    for reviewer in ("qa-review-agent", "code-review-agent"):
        definition = agents.get(reviewer)
        if definition and definition.config.get("permissionMode") != "plan":
            errors.append(f"{definition.path}: reviewer must use permissionMode: plan")
    return agents, errors


def _parse_inline_list(value: str, number: int) -> list[str]:
    """Phân tích danh sách YAML một dòng dùng cho required_skills."""

    value = value.strip()
    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError(f"required_skills must be an inline list at line {number}")
    body = value[1:-1].strip()
    if not body:
        return []
    return [item.strip().strip("'\"") for item in body.split(",") if item.strip()]


def parse_workflow(path: Path) -> dict[str, dict[str, WorkflowStep]]:
    """Đọc ánh xạ stage-step-agent-skill từ YAML con được skill hỗ trợ."""

    raw: dict[str, dict[str, dict[str, object]]] = {}
    current_stage: str | None = None
    current_step: str | None = None
    in_stages = False
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        clean = line.split("#", 1)[0].rstrip()
        if not clean:
            continue
        indent = len(clean) - len(clean.lstrip(" "))
        stripped = clean.strip()
        if indent == 0 and stripped == "stages:":
            in_stages = True
            continue
        if not in_stages:
            continue
        if indent == 2 and stripped.endswith(":"):
            current_stage = stripped[:-1]
            current_step = None
            raw[current_stage] = {}
            continue
        if indent == 4 and current_stage and stripped.endswith(":"):
            current_step = stripped[:-1]
            raw[current_stage][current_step] = {}
            continue
        if indent == 6 and current_stage and current_step and ":" in stripped:
            key, value = (part.strip() for part in stripped.split(":", 1))
            if key == "agent":
                raw[current_stage][current_step][key] = value.strip("'\"")
            elif key == "required_skills":
                raw[current_stage][current_step][key] = _parse_inline_list(value, number)
            else:
                raise ValueError(f"unknown workflow field at line {number}: {key}")
            continue
        raise ValueError(f"invalid workflow structure at line {number}: {line}")

    result: dict[str, dict[str, WorkflowStep]] = {}
    for stage, steps in raw.items():
        result[stage] = {}
        for step, fields in steps.items():
            if not isinstance(fields.get("agent"), str):
                raise ValueError(f"workflow {stage}.{step} missing agent")
            if not isinstance(fields.get("required_skills"), list):
                raise ValueError(f"workflow {stage}.{step} missing required_skills")
            result[stage][step] = WorkflowStep(
                agent=str(fields["agent"]),
                required_skills=[str(item) for item in fields["required_skills"]],
            )
    return result


def validate_companion_skills(skill_source_root: Path) -> list[str]:
    """Kiểm tra companion skill có SKILL.md và frontmatter Claude hợp lệ."""

    errors: list[str] = []
    discovered = {path.name for path in skill_source_root.glob("sdlc-*") if path.is_dir()}
    missing = sorted(EXPECTED_SKILLS - discovered)
    extra = sorted(discovered - EXPECTED_SKILLS)
    if missing:
        errors.append("missing companion skills: " + ", ".join(missing))
    if extra:
        errors.append("unexpected companion skills: " + ", ".join(extra))
    for skill_name in sorted(EXPECTED_SKILLS & discovered):
        path = skill_source_root / skill_name / "SKILL.md"
        if not path.is_file():
            errors.append(f"{path}: SKILL.md not found")
            continue
        try:
            frontmatter = parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        declared_name = str(frontmatter.get("name", ""))
        if declared_name != skill_name:
            errors.append(f"{path}: name must match directory {skill_name}")
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{path}: description must be a non-empty string")
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for required_section in REQUIRED_DISCOVERY_SECTIONS.get(skill_name, ()):
            if required_section not in "\n".join(lines):
                errors.append(f"{path}: missing guided-discovery section: {required_section}")
        skill_text = "\n".join(lines)
        for marker in REQUIRED_CONTEXT_MARKERS.get(skill_name, ()):
            if marker not in skill_text:
                errors.append(f"{path}: missing migrated stage context: {marker}")
    return errors


def validate_stage_contracts(skill_root: Path) -> list[str]:
    """Kiểm tra bảy stage reference chỉ dùng cấu trúc contract thống nhất."""

    errors: list[str] = []
    for stage in STAGES:
        path = skill_root / "references" / f"{stage}.md"
        if not path.is_file():
            errors.append(f"{path}: stage contract not found")
            continue
        text = path.read_text(encoding="utf-8-sig")
        headings = tuple(line for line in text.splitlines() if line.startswith("## "))
        if headings != STAGE_CONTRACT_HEADINGS:
            errors.append(f"{path}: stage contract headings do not match required structure")
        for legacy_heading in ("Nguyên tắc của giai đoạn", "Quy tắc thực hiện", "Kiểm tra chất lượng"):
            if legacy_heading in text:
                errors.append(f"{path}: operational guidance must move to companion skill: {legacy_heading}")
        if "guided-discovery.md" in text:
            errors.append(f"{path}: obsolete guided-discovery reference")
    return errors


def parse_bindings(path: Path) -> dict[str, str]:
    """Đọc target của từng agent từ file cấu hình dự án."""

    bindings: dict[str, str] = {}
    current_agent: str | None = None
    in_bindings = False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        clean = line.split("#", 1)[0].rstrip()
        if not clean:
            continue
        indent = len(clean) - len(clean.lstrip(" "))
        stripped = clean.strip()
        if indent == 0 and stripped == "agent_bindings:":
            in_bindings = True
            continue
        if not in_bindings:
            continue
        if indent == 2 and stripped.endswith(":"):
            current_agent = stripped[:-1]
            continue
        if indent == 4 and current_agent and stripped.startswith("target:"):
            bindings[current_agent] = stripped.split(":", 1)[1].strip().strip("'\"")
    return bindings


def validate(
    skill_root: Path,
    config_path: Path | None = None,
    project_root: Path | None = None,
) -> list[str]:
    """Kiểm tra agent, companion skill, workflow, human gate và separation."""

    resolved_project_root = (project_root or Path.cwd()).resolve()
    project_agents = resolved_project_root / ".claude" / "agents"
    agent_directory = project_agents if project_agents.is_dir() else Path.home() / ".claude" / "agents"
    agents, errors = load_agents(agent_directory)
    errors.extend(validate_companion_skills(skill_root.parent))
    errors.extend(validate_stage_contracts(skill_root))

    workflow_path = skill_root / "references" / "agent-workflow.yaml"
    try:
        workflow = parse_workflow(workflow_path)
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{workflow_path}: {exc}")
        workflow = {}

    for stage in STAGES:
        mapping = workflow.get(stage)
        if mapping is None:
            errors.append(f"workflow missing stage: {stage}")
            continue
        missing_steps = sorted(set(STEPS) - mapping.keys())
        extra_steps = sorted(mapping.keys() - set(STEPS))
        if missing_steps:
            errors.append(f"workflow {stage} missing steps: {', '.join(missing_steps)}")
        if extra_steps:
            errors.append(f"workflow {stage} unknown steps: {', '.join(extra_steps)}")
        for step, assignment in mapping.items():
            if step == "human_gate":
                if assignment.agent != "human":
                    errors.append(f"workflow {stage}.human_gate must be human")
                if assignment.required_skills:
                    errors.append(f"workflow {stage}.human_gate cannot require skills")
            elif assignment.agent not in agents:
                errors.append(f"workflow {stage}.{step} references unknown agent: {assignment.agent}")
            unknown_skills = sorted(set(assignment.required_skills) - EXPECTED_SKILLS)
            if unknown_skills:
                errors.append(f"workflow {stage}.{step} references unknown skills: {', '.join(unknown_skills)}")

    for (stage, step), (agent_name, skills) in EXPECTED_ASSIGNMENTS.items():
        assignment = workflow.get(stage, {}).get(step)
        if assignment is None or assignment.agent != agent_name or assignment.required_skills != skills:
            errors.append(f"workflow {stage}.{step} must use {agent_name} with {', '.join(skills)}")

    if config_path and config_path.exists():
        bindings = parse_bindings(config_path)
        for agent_name in bindings:
            if agent_name not in agents:
                errors.append(f"{config_path}: binding references unknown agent: {agent_name}")
        for executor, reviewer in (
            ("qa-agent", "qa-review-agent"),
            ("development-agent", "code-review-agent"),
        ):
            if bindings.get(executor) and bindings.get(executor) == bindings.get(reviewer):
                errors.append(
                    f"{config_path}: strict separation violated: {executor} and {reviewer} "
                    f"share target {bindings[executor]}"
                )
    return errors


def main() -> int:
    """Chạy validator agent từ dòng lệnh và trả mã thoát tương ứng."""

    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    config_path = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    project_root = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    errors = validate(skill_root, config_path, project_root)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"FAILED: {len(errors)} agent/workflow/skill error(s)")
        return 1
    print("OK: 5 Claude Code agents, 10 companion skills and 7-stage workflow validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
