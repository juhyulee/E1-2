"""Domain models used by the quiz game."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Quiz:
    """Represent one four-choice quiz question."""

    question: str
    choices: list[str]
    answer: int
    hint: str = ""

    def __post_init__(self) -> None:
        self.question = self.question.strip()
        self.choices = [str(choice).strip() for choice in self.choices]
        self.hint = self.hint.strip()

        if not self.question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(self.choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if any(not choice for choice in self.choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if self.answer not in range(1, 5):
            raise ValueError("정답은 1부터 4 사이여야 합니다.")

    def format_question(self, number: int | None = None) -> str:
        """Return a display-ready question and its numbered choices."""
        heading = f"Q{number}. {self.question}" if number else self.question
        choice_lines = [
            f"  {index}. {choice}"
            for index, choice in enumerate(self.choices, start=1)
        ]
        return "\n".join([heading, *choice_lines])

    def is_correct(self, selected_answer: int) -> bool:
        """Return whether a selected choice number is correct."""
        return selected_answer == self.answer

    @property
    def correct_choice(self) -> str:
        """Return the text for the correct choice."""
        return self.choices[self.answer - 1]

    def to_dict(self) -> dict[str, Any]:
        """Convert this object to JSON-serializable data."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        """Build a validated quiz from decoded JSON data."""
        return cls(
            question=str(data["question"]),
            choices=list(data["choices"]),
            answer=int(data["answer"]),
            hint=str(data.get("hint", "")),
        )


