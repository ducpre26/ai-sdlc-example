#!/usr/bin/env python3
"""Kiểm tra artifact Markdown AI-First SDLC mà không cần thư viện ngoài."""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


REQUIRED = {
    "document_id", "document_type", "project", "version", "supersedes_version", "status",
    "previous_status", "owner", "approver", "created_at", "updated_at",
    "source_documents", "related_documents", "related_work_items", "evidence",
    "open_questions", "ai_generated", "ai_checked_at", "human_decision",
    "human_approved_at",
}
STATUSES = ["draft", "ai_checked", "human_review", "approved", "superseded"]
ALLOWED_TRANSITIONS = {
    (None, "draft"),
    ("draft", "ai_checked"),
    ("ai_checked", "human_review"),
    ("human_review", "approved"),
    ("approved", "superseded"),
}
DATE_FIELDS = {"created_at", "updated_at", "ai_checked_at", "human_approved_at"}
LIST_FIELDS = {
    "source_documents", "related_documents", "related_work_items",
    "evidence", "open_questions",
}
PLACEHOLDER_RE = re.compile(r"\bTBD\b|\{[^{}]+\}|<placeholder>", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
VERSION_RE = re.compile(r"\d+\.\d+\.\d+")
VERSIONED_REFERENCE_RE = re.compile(r"^([A-Z][A-Z0-9-]{2,63})@(\d+\.\d+\.\d+)$")
VERSIONED_FILENAME_RE = re.compile(r"-v\d+\.\d+\.\d+(?=\.[^.]+$)", re.IGNORECASE)


@dataclass
class Artifact:
    """Biểu diễn artifact gồm đường dẫn, metadata và nội dung Markdown."""

    path: Path
    metadata: dict[str, object]
    body: str


def scalar(value: str) -> object:
    """Chuyển một giá trị YAML đơn giản thành kiểu Python tương ứng."""

    value = value.strip()
    if value in {"", "null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            inner = value[1:-1].strip()
            parsed = [] if not inner else [x.strip().strip("'\"") for x in inner.split(",")]
        if not isinstance(parsed, list):
            raise ValueError("array value must be a list")
        return parsed
    if (value.startswith("\"") and value.endswith("\"")) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_artifact_text(text: str, path: Path) -> Artifact:
    """Phân tích frontmatter và nội dung artifact từ chuỗi Markdown."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML front matter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing YAML front matter delimiter") from exc
    metadata: dict[str, object] = {}
    index = 1
    while index < end:
        line = lines[index]
        number = index + 1
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if ":" not in line:
            raise ValueError(f"invalid YAML subset at line {number}: expected key: value")
        key, raw = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ValueError(f"invalid metadata key at line {number}: {key}")
        if key in metadata:
            raise ValueError(f"duplicate metadata key at line {number}: {key}")
        if not raw.strip():
            items: list[object] = []
            cursor = index + 1
            while cursor < end and lines[cursor].startswith(("  - ", "    - ")):
                items.append(scalar(lines[cursor].split("-", 1)[1]))
                cursor += 1
            if items:
                metadata[key] = items
                index = cursor
                continue
        metadata[key] = scalar(raw)
        index += 1
    return Artifact(path=path, metadata=metadata, body="\n".join(lines[end + 1 :]))


def parse_artifact(path: Path) -> Artifact:
    """Đọc và phân tích một artifact Markdown từ filesystem."""

    return parse_artifact_text(path.read_text(encoding="utf-8-sig"), path)


def valid_date(value: object) -> bool:
    """Kiểm tra giá trị ngày có dạng YYYY-MM-DD hoặc null."""

    if value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    except ValueError:
        return False


def version_tuple(value: object) -> tuple[int, int, int] | None:
    """Chuyển semantic version hợp lệ thành bộ ba số nguyên."""

    if not isinstance(value, str) or not VERSION_RE.fullmatch(value):
        return None
    return tuple(int(part) for part in value.split("."))


def validate_reference(
    reference: object,
    field: str,
    known_ids: set[str],
    known_versions: set[tuple[str, str]],
) -> str | None:
    """Kiểm tra một tham chiếu document ID hoặc document ID kèm version."""

    if not isinstance(reference, str):
        return f"{field} reference must be a string: {reference}"
    versioned = VERSIONED_REFERENCE_RE.fullmatch(reference)
    if versioned:
        key = (versioned.group(1), versioned.group(2))
        if key not in known_versions:
            return f"unknown {field} reference: {reference}"
        return None
    if reference not in known_ids:
        return f"unknown {field} reference: {reference}"
    return None


def validate_artifact(
    artifact: Artifact,
    known_ids: set[str],
    known_versions: set[tuple[str, str]],
) -> list[str]:
    """Kiểm tra metadata, lifecycle, traceability và liên kết của một artifact."""

    m = artifact.metadata
    errors: list[str] = []
    missing = sorted(REQUIRED - m.keys())
    if missing:
        errors.append(f"missing metadata: {', '.join(missing)}")
        return errors

    doc_id = m["document_id"]
    if not isinstance(doc_id, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{2,63}", doc_id):
        errors.append("document_id must match ^[A-Z][A-Z0-9-]{2,63}$")
    if not isinstance(m["document_type"], str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", m["document_type"]):
        errors.append("document_type must be lowercase kebab-case")
    current_version = version_tuple(m["version"])
    if current_version is None:
        errors.append("version must use semantic form x.y.z")
    supersedes_version = m["supersedes_version"]
    if supersedes_version is not None:
        superseded = version_tuple(supersedes_version)
        if superseded is None:
            errors.append("supersedes_version must use semantic form x.y.z or null")
        elif current_version is not None and superseded >= current_version:
            errors.append("supersedes_version must be lower than version")
        elif isinstance(doc_id, str) and (doc_id, str(supersedes_version)) not in known_versions:
            errors.append(f"supersedes_version does not resolve in worktree or Git history: {doc_id}@{supersedes_version}")
    if m["status"] not in STATUSES:
        errors.append(f"invalid status: {m['status']}")
    if (m["previous_status"], m["status"]) not in ALLOWED_TRANSITIONS:
        errors.append(f"invalid transition: {m['previous_status']} → {m['status']}")
    for field in DATE_FIELDS:
        if not valid_date(m[field]):
            errors.append(f"{field} must be YYYY-MM-DD or null")
    for field in LIST_FIELDS:
        if not isinstance(m[field], list):
            errors.append(f"{field} must be an inline YAML array")
    if not isinstance(m["ai_generated"], bool):
        errors.append("ai_generated must be true or false")

    if m["status"] in {"ai_checked", "human_review", "approved", "superseded"} and not m["ai_checked_at"]:
        errors.append("ai_checked_at is required after draft")
    if m["status"] == "approved":
        if m["human_decision"] != "approved" or not m["human_approved_at"]:
            errors.append("approved document requires human_decision and human_approved_at")
        if str(m["approver"]).lower().startswith(("ai", "agent", "bot")):
            errors.append("AI/bot cannot be the approver")
        if m["open_questions"]:
            errors.append("approved document cannot contain open_questions")
        if PLACEHOLDER_RE.search(artifact.body) or any(
            PLACEHOLDER_RE.search(str(value)) for value in m.values()
        ):
            errors.append("approved document contains TBD or placeholder")

    for field in ("source_documents", "related_documents"):
        if isinstance(m[field], list):
            for reference in m[field]:
                message = validate_reference(reference, field, known_ids, known_versions)
                if message:
                    errors.append(message)

    for target in LINK_RE.findall(artifact.body):
        clean = target.split("#", 1)[0].replace("%20", " ")
        if clean and not (artifact.path.parent / clean).resolve().exists():
            errors.append(f"broken local Markdown link: {target}")

    if m["document_type"] == "requirements-traceability-matrix" and m["status"] == "approved":
        rows = [line for line in artifact.body.splitlines() if re.match(r"^\|\s*BO-\d+", line)]
        if not rows:
            errors.append("approved RTM requires at least one BO traceability row")
        for row in rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            if len(cells) < 7 or any(not cell for cell in cells[:7]):
                errors.append(f"incomplete traceability row: {row}")
    return errors


def run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Chạy lệnh Git trong repository và thu lại stdout cùng stderr dạng UTF-8."""

    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def find_git_root(path: Path) -> Path | None:
    """Tìm Git repository bao quanh một file hoặc thư mục."""

    start = path if path.is_dir() else path.parent
    result = run_git(start, "rev-parse", "--show-toplevel")
    if result.returncode:
        return None
    return Path(result.stdout.strip()).resolve()


def relative_git_path(repo_root: Path, path: Path) -> str:
    """Trả đường dẫn POSIX của file tương đối với Git root."""

    return path.resolve().relative_to(repo_root).as_posix()


def artifact_is_committed(repo_root: Path, path: Path) -> bool:
    """Xác nhận artifact đã được theo dõi và không khác HEAD ở index/worktree."""

    relative = relative_git_path(repo_root, path)
    tracked = run_git(repo_root, "ls-files", "--error-unmatch", "--", relative)
    if tracked.returncode:
        return False
    unstaged = run_git(repo_root, "diff", "--quiet", "HEAD", "--", relative)
    staged = run_git(repo_root, "diff", "--cached", "--quiet", "HEAD", "--", relative)
    return unstaged.returncode == 0 and staged.returncode == 0


def git_history_versions(repo_root: Path, docs_root: Path) -> set[tuple[str, str]]:
    """Lập chỉ mục document ID và version từ Markdown đã commit trong Git."""
    relative_root = relative_git_path(repo_root, docs_root)
    log = run_git(repo_root, "log", "--all", "--format=%H", "--", relative_root)
    if log.returncode:
        return set()
    versions: set[tuple[str, str]] = set()
    for commit in dict.fromkeys(line.strip() for line in log.stdout.splitlines() if line.strip()):
        tree = run_git(repo_root, "ls-tree", "-r", "--name-only", commit, "--", relative_root)
        if tree.returncode:
            continue
        for relative in tree.stdout.splitlines():
            if not relative.lower().endswith(".md") or Path(relative).name.lower() == "_progress.md":
                continue
            shown = run_git(repo_root, "show", f"{commit}:{relative}")
            if shown.returncode:
                continue
            try:
                artifact = parse_artifact_text(shown.stdout, repo_root / relative)
            except (UnicodeError, ValueError):
                continue
            doc_id = artifact.metadata.get("document_id")
            version = artifact.metadata.get("version")
            if isinstance(doc_id, str) and isinstance(version, str):
                versions.add((doc_id, version))
    return versions


def markdown_files(inputs: list[str]) -> list[Path]:
    """Thu thập các file Markdown artifact từ danh sách file hoặc thư mục."""

    files: set[Path] = set()
    for raw in inputs:
        path = Path(raw)
        if path.is_file() and is_artifact_markdown(path):
            files.add(path.resolve())
        elif path.is_dir():
            files.update(p.resolve() for p in path.rglob("*.md") if is_artifact_markdown(p))
    return sorted(files)


def is_artifact_markdown(path: Path) -> bool:
    """Xác định file Markdown có phải artifact thay vì file tiến độ hay không."""

    return path.suffix.lower() == ".md" and path.name.lower() != "_progress.md"


def validate_collection(
    artifacts: list[Artifact],
    historical_versions: set[tuple[str, str]] | None = None,
) -> tuple[list[tuple[Path, str]], int]:
    """Kiểm tra tính duy nhất và tham chiếu xuyên suốt một tập artifact."""

    errors: list[tuple[Path, str]] = []
    versions: dict[tuple[str, str], Path] = {}
    document_types: dict[str, str] = {}
    live_documents: dict[str, Path] = {}
    for artifact in artifacts:
        doc_id = artifact.metadata.get("document_id")
        version = artifact.metadata.get("version")
        document_type = artifact.metadata.get("document_type")
        if isinstance(doc_id, str) and isinstance(version, str):
            key = (doc_id, version)
            if key in versions:
                errors.append((artifact.path, f"duplicate document_id and version also used by {versions[key]}: {doc_id}@{version}"))
            else:
                versions[key] = artifact.path
        if isinstance(doc_id, str) and isinstance(document_type, str):
            existing_type = document_types.get(doc_id)
            if existing_type is not None and existing_type != document_type:
                errors.append((artifact.path, f"document_id changes document_type across versions: {doc_id}"))
            else:
                document_types[doc_id] = document_type
        if isinstance(doc_id, str):
            existing_path = live_documents.get(doc_id)
            if existing_path is not None and existing_path != artifact.path:
                errors.append((artifact.path, f"multiple live files for one document_id; keep one stable filename: {doc_id} ({existing_path}, {artifact.path})"))
            else:
                live_documents[doc_id] = artifact.path
        if VERSIONED_FILENAME_RE.search(artifact.path.name):
            errors.append((artifact.path, "versioned filename is legacy; keep version in metadata and use one stable filename"))

    known_ids = set(document_types)
    known_versions = set(versions) | (historical_versions or set())
    for artifact in artifacts:
        for message in validate_artifact(artifact, known_ids, known_versions):
            errors.append((artifact.path, message))
    return errors, len(document_types)


def main() -> int:
    """Chạy artifact validator từ dòng lệnh và trả mã thoát tương ứng."""

    arguments = sys.argv[1:]
    no_git_history = "--no-git-history" in arguments
    allow_uncommitted_approved = "--allow-uncommitted-approved" in arguments
    options = {"--no-git-history", "--allow-uncommitted-approved"}
    raw_inputs = [argument for argument in arguments if argument not in options] or ["templates", "examples"]
    input_paths = [Path(raw) for raw in raw_inputs]
    paths = markdown_files(raw_inputs)
    if not paths:
        print("ERROR: no Markdown artifacts found")
        return 2
    artifacts: list[Artifact] = []
    errors: list[tuple[Path, str]] = []
    for path in paths:
        try:
            artifacts.append(parse_artifact(path))
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append((path, str(exc)))

    docs_root = next((path.resolve() for path in input_paths if path.is_dir() and (
        path.name.lower() == "ai-sdlc" or (path / "_progress.md").exists()
    )), None)
    historical_versions: set[tuple[str, str]] = set()
    repo_root: Path | None = None
    if docs_root is not None and not no_git_history:
        repo_root = find_git_root(docs_root)
        if repo_root is None:
            errors.append((docs_root, "Git repository is required; ask before running git init"))
        else:
            historical_versions = git_history_versions(repo_root, docs_root)

    validation_errors, unique_document_ids = validate_collection(artifacts, historical_versions)
    errors.extend(validation_errors)
    if repo_root is not None and not allow_uncommitted_approved:
        for artifact in artifacts:
            if artifact.metadata.get("status") == "approved" and not artifact_is_committed(repo_root, artifact.path):
                errors.append((artifact.path, "approved baseline must be committed before downstream use"))

    if errors:
        for path, message in errors:
            print(f"ERROR {path}: {message}")
        print(f"FAILED: {len(errors)} error(s), {len(artifacts)} parsed artifact(s)")
        return 1
    print(f"OK: {len(artifacts)} live artifact(s) validated; {unique_document_ids} unique document ID(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
