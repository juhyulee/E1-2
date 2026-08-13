from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from quiz_game.models import Quiz
from quiz_game.storage import GameState, StateRepository


class StateRepositoryTests(unittest.TestCase):
    def test_missing_file_uses_default_quizzes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = StateRepository(Path(directory) / "state.json")

            state = repository.load()

            self.assertGreaterEqual(len(state.quizzes), 5)
            self.assertIn("없어 기본 퀴즈", repository.last_message)

    def test_corrupt_file_is_backed_up_and_recovers_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            state_path.write_text("{not valid json", encoding="utf-8")
            repository = StateRepository(state_path)

            state = repository.load()

            self.assertGreaterEqual(len(state.quizzes), 5)
            self.assertIn("손상되어 기본 데이터", repository.last_message)
            self.assertFalse(state_path.exists())
            self.assertEqual(len(list(Path(directory).glob("state.json.corrupt-*"))), 1)

    def test_utf8_round_trip_preserves_korean_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            repository = StateRepository(state_path)
            state = GameState(
                quizzes=[Quiz("한글 문제", ["하나", "둘", "셋", "넷"], 3)],
                best_score=1,
                best_total=1,
                score_history=[
                    {"played_at": "2026-08-13T12:00:00", "score": 1, "total": 1}
                ],
            )

            self.assertTrue(repository.save(state))
            decoded = json.loads(state_path.read_text(encoding="utf-8"))
            reloaded = repository.load()

            self.assertEqual(decoded["quizzes"][0]["question"], "한글 문제")
            self.assertEqual(reloaded.quizzes[0].choices[2], "셋")
            self.assertEqual(reloaded.best_score, 1)


if __name__ == "__main__":
    unittest.main()
