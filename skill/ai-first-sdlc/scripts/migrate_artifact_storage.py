#!/usr/bin/env python3
"""Hợp nhất artifact SDLC có hậu tố phiên bản thành file hiện hành ổn định."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


VALIDATOR_PATH = Path(__file__).with_name("validate_artifacts.py")
SPEC = importlib.util.spec_from_file_location("validate_artifacts_for_migration", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load validate_artifacts.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

VERSION_SUFFIX_RE = re.compile(r"-v(\d+\.\d+\.\d+)(?=\.[^.]+$)", re.IGNORECASE)
OPENAPI_VERSION_RE = re.compile(r"(?m)^\s{2}version:\s*['\"]?(\d+\.\d+\.\d+)['\"]?\s*$")


@dataclass
class Candidate:
    """Mô tả một phiên bản artifact được cân nhắc trong quá trình migration."""

    key: str
    version: tuple[int, int, int]
    version_text: str
    path: Path
    target: Path


def stable_name(path: Path) -> str:
    """Loại hậu tố semantic version khỏi tên file artifact."""

    return VERSION_SUFFIX_RE.sub("", path.name)


def discover(docs_root: Path) -> tuple[dict[str, list[Candidate]], list[str]]:
    """Tìm và nhóm các artifact theo document ID hoặc khóa OpenAPI tương đương."""

    groups: dict[str, list[Candidate]] = {}
    errors: list[str] = []
    for path in sorted(docs_root.rglob("*.md")):
        if path.name.lower() == "_progress.md":
            continue
        try:
            artifact = VALIDATOR.parse_artifact(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        doc_id = artifact.metadata.get("document_id")
        version_text = artifact.metadata.get("version")
        version = VALIDATOR.version_tuple(version_text)
        if not isinstance(doc_id, str) or version is None:
            errors.append(f"{path}: missing valid document_id/version")
            continue
        target = path.with_name(stable_name(path))
        groups.setdefault(doc_id, []).append(Candidate(doc_id, version, str(version_text), path, target))

    for path in sorted(docs_root.rglob("*.yaml")):
        canonical = path.with_name(stable_name(path))
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        document_id: str | None = None
        version_text: str | None = None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            document_id = parsed.get("x-document-id") if isinstance(parsed.get("x-document-id"), str) else None
            raw_version = parsed.get("x-document-version")
            if not isinstance(raw_version, str):
                info = parsed.get("info")
                raw_version = info.get("version") if isinstance(info, dict) else None
            version_text = raw_version if isinstance(raw_version, str) else None
        if version_text is None:
            match = OPENAPI_VERSION_RE.search(text)
            version_text = match.group(1) if match else None
        if version_text is None:
            continue
        key = document_id or ("yaml:" + canonical.as_posix().lower())
        version = VALIDATOR.version_tuple(version_text)
        if version is not None:
            groups.setdefault(key, []).append(Candidate(key, version, version_text, path, canonical))
    return groups, errors


def git_clean_and_tracked(repo_root: Path, path: Path) -> bool:
    """Kiểm tra file đã được Git theo dõi, commit và không có thay đổi cục bộ."""

    return VALIDATOR.artifact_is_committed(repo_root, path)


def plan(groups: dict[str, list[Candidate]]) -> list[tuple[str, Candidate, list[Candidate]]]:
    """Chọn phiên bản hiện hành và đường dẫn ổn định cho từng nhóm artifact."""

    result: list[tuple[str, Candidate, list[Candidate]]] = []
    for key, candidates in sorted(groups.items()):
        if len({candidate.version_text for candidate in candidates}) != len(candidates):
            raise ValueError(f"duplicate version in {key}")
        latest = max(candidates, key=lambda candidate: candidate.version)
        canonical = latest.path.with_name(stable_name(latest.path))
        latest = Candidate(latest.key, latest.version, latest.version_text, latest.path, canonical)
        result.append((key, latest, candidates))
    return result


def apply_plan(items: list[tuple[str, Candidate, list[Candidate]]]) -> None:
    """Áp dụng kế hoạch bằng cách giữ bản mới nhất và xóa các file phiên bản cũ."""

    for _, latest, candidates in items:
        target = latest.target
        if latest.path.resolve() != target.resolve():
            shutil.copy2(latest.path, target)
        for candidate in candidates:
            if candidate.path.resolve() != target.resolve() and candidate.path.exists():
                candidate.path.unlink()


def main() -> int:
    """Chạy migration ở chế độ dry-run hoặc apply có kiểm tra an toàn Git."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_root", type=Path)
    parser.add_argument("--apply", action="store_true", help="apply the migration; default is dry-run")
    args = parser.parse_args()
    docs_root = args.docs_root.resolve()
    if not docs_root.is_dir():
        print(f"ERROR: docs root not found: {docs_root}")
        return 2
    groups, errors = discover(docs_root)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"BLOCKED: fix {len(errors)} metadata/parse error(s) before migration")
        return 1
    try:
        items = plan(groups)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("# Artifact storage migration")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    for key, latest, candidates in items:
        if len(candidates) == 1 and candidates[0].path.name == latest.target.name:
            continue
        versions = ", ".join(candidate.version_text for candidate in sorted(candidates, key=lambda item: item.version))
        removed = [candidate.path.name for candidate in candidates if candidate.path.resolve() != latest.target.resolve()]
        print(f"- {key}: versions [{versions}] → {latest.target}")
        print(f"  current: {latest.path.name}@{latest.version_text}")
        print(f"  remove from worktree: {', '.join(removed) if removed else 'none'}")
    if not args.apply:
        print("DRY-RUN complete; no files changed")
        return 0

    repo_root = VALIDATOR.find_git_root(docs_root)
    if repo_root is None:
        print("ERROR: Git repository is required; ask before running git init")
        return 1
    affected = {candidate.path for _, _, candidates in items for candidate in candidates}
    uncommitted = sorted(path for path in affected if not git_clean_and_tracked(repo_root, path))
    if uncommitted:
        for path in uncommitted:
            print(f"ERROR {path}: legacy file must be tracked and clean in a safety commit")
        return 1
    apply_plan(items)
    validator = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--allow-uncommitted-approved", str(docs_root)],
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if validator.stdout:
        print(validator.stdout, end="")
    if validator.stderr:
        print(validator.stderr, end="", file=sys.stderr)
    if validator.returncode == 0:
        print("Migration applied and structurally validated. Commit the stable files, then run the normal validator before downstream use.")
    return validator.returncode


if __name__ == "__main__":
    raise SystemExit(main())
