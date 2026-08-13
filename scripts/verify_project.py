"""Verify mission requirements using only the Python standard library."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
STATE = ROOT / "state.json"


def check_state() -> None:
    """Validate the documented state.json schema and default questions."""
    data = json.loads(STATE.read_text(encoding="utf-8"))
    required_keys = {"quizzes", "best_score", "best_total", "score_history"}
    assert required_keys <= data.keys(), "state.json 필수 키가 없습니다."
    assert len(data["quizzes"]) >= 5, "기본 퀴즈는 5개 이상이어야 합니다."
    assert all(
        len(quiz["choices"]) == 4 and 1 <= quiz["answer"] <= 4
        for quiz in data["quizzes"]
    ), "각 퀴즈는 선택지 4개와 1~4 정답 번호가 필요합니다."
    print(f"PASS state: {len(data['quizzes'])} quizzes and valid schema")


def check_readme() -> None:
    """Check mandatory README sections and local links."""
    content = README.read_text(encoding="utf-8")
    required_sections = (
        "프로젝트 개요",
        "퀴즈 주제",
        "실행 방법",
        "기능 목록",
        "파일 구조",
        "state.json",
    )
    missing_sections = [item for item in required_sections if item not in content]
    assert not missing_sections, f"README 필수 항목 누락: {missing_sections}"

    link_targets = re.findall(r"]\((?!https?://|#)([^)]+)\)", content)
    missing_links = [target for target in link_targets if not (ROOT / target).exists()]
    assert not missing_links, f"README 링크 대상 누락: {missing_links}"
    print("PASS README: required sections and relative links")


def git(*arguments: str) -> str:
    """Run a read-only Git command and return its output."""
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def check_git_history() -> None:
    """Verify commit count and the feature branch merge ancestry."""
    commit_count = int(git("rev-list", "--count", "HEAD"))
    assert commit_count >= 10, "의미 있는 커밋이 10개 이상이어야 합니다."
    git("merge-base", "--is-ancestor", "37e9e87", "main")
    merge_log = git("log", "--merges", "--oneline")
    assert "merge: integrate quiz play feature" in merge_log
    print(f"PASS Git: {commit_count} commits and quiz feature merge")


def check_secrets() -> None:
    """Search tracked text files for common credential signatures."""
    patterns = (
        re.compile(r"ghp_[A-Za-z0-9]{20,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]+"),
        re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    )
    tracked_files = git("ls-files").splitlines()
    findings: list[str] = []
    for relative_path in tracked_files:
        path = ROOT / relative_path
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(pattern.search(content) for pattern in patterns):
            findings.append(relative_path)
    assert not findings, f"민감정보 의심 파일: {findings}"
    print("PASS security: no common credential signatures")


def main() -> int:
    """Run every verification and return a process exit code."""
    try:
        check_state()
        check_readme()
        check_git_history()
        check_secrets()
    except (AssertionError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
