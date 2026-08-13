"""UTF-8 JSON persistence for quizzes and score history."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from quiz_game.defaults import create_default_quizzes
from quiz_game.models import Quiz


@dataclass(slots=True)
class GameState:
    """All data that must survive between program runs."""

    quizzes: list[Quiz] = field(default_factory=create_default_quizzes)
    best_score: int = 0
    best_total: int = 0
    score_history: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert the state to the documented JSON schema."""
        return {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_total": self.best_total,
            "score_history": list(self.score_history),
        }


class StateRepository:
    """Load and save game state at the project root."""

    def __init__(self, path: str | Path = "state.json") -> None:
        self.path = Path(path)
        self.last_message = ""

    def load(self) -> GameState:
        """Load validated state, recovering with defaults when necessary."""
        if not self.path.exists():
            self.last_message = "state.json이 없어 기본 퀴즈로 시작합니다."
            return GameState()

        try:
            with self.path.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)
            state = self._decode_state(raw_data)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            backup = self._backup_corrupt_file()
            backup_notice = f" 손상 파일 백업: {backup.name}" if backup else ""
            self.last_message = (
                "state.json이 손상되어 기본 데이터로 복구했습니다."
                f"{backup_notice} ({type(error).__name__})"
            )
            return GameState()
        except OSError as error:
            self.last_message = (
                "state.json을 읽을 수 없어 기본 데이터로 시작합니다: "
                f"{error}"
            )
            return GameState()

        self.last_message = f"state.json에서 퀴즈 {len(state.quizzes)}개를 불러왔습니다."
        return state

    def save(self, state: GameState) -> bool:
        """Atomically save UTF-8 JSON and report whether it succeeded."""
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
                json.dump(state.to_dict(), file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary_path.replace(self.path)
        except OSError as error:
            self.last_message = f"데이터 저장에 실패했습니다: {error}"
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
            return False

        self.last_message = f"데이터를 {self.path}에 저장했습니다."
        return True

    @staticmethod
    def _decode_state(raw_data: Any) -> GameState:
        if not isinstance(raw_data, dict):
            raise TypeError("최상위 JSON 값은 객체여야 합니다.")

        raw_quizzes = raw_data["quizzes"]
        if not isinstance(raw_quizzes, list):
            raise TypeError("quizzes는 배열이어야 합니다.")

        quizzes = [Quiz.from_dict(item) for item in raw_quizzes]
        best_score = int(raw_data.get("best_score", 0))
        best_total = int(raw_data.get("best_total", 0))
        history = raw_data.get("score_history", [])

        if best_score < 0 or best_total < 0 or best_score > best_total:
            raise ValueError("최고 점수 범위가 올바르지 않습니다.")
        if not isinstance(history, list):
            raise TypeError("score_history는 배열이어야 합니다.")

        return GameState(
            quizzes=quizzes,
            best_score=best_score,
            best_total=best_total,
            score_history=history,
        )

    def _backup_corrupt_file(self) -> Path | None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = self.path.with_name(f"{self.path.name}.corrupt-{timestamp}")
        try:
            self.path.replace(backup_path)
        except OSError:
            return None
        return backup_path


