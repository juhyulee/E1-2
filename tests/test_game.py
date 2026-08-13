from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from quiz_game.console import Console
from quiz_game.game import QuizGame
from quiz_game.storage import StateRepository


class ScriptedIO:
    def __init__(self, answers: list[str]) -> None:
        self.answers = iter(answers)
        self.output: list[str] = []

    def input(self, prompt: str) -> str:
        self.output.append(prompt)
        return next(self.answers)

    def print(self, message: str) -> None:
        self.output.append(message)


class QuizPlayTests(unittest.TestCase):
    def test_play_quiz_records_score_and_best_score(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = StateRepository(Path(directory) / "state.json")
            io = ScriptedIO(["2", "2", "2"])
            game = QuizGame(Console(io.input, io.print), repository)

            chosen = [game.quizzes[0], game.quizzes[1]]
            with patch("quiz_game.game.random.sample", return_value=chosen):
                game.play_quiz()

            self.assertEqual(game.state.best_score, 2)
            self.assertEqual(game.state.best_total, 2)
            self.assertEqual(len(game.state.score_history), 1)
            self.assertTrue((Path(directory) / "state.json").exists())
            self.assertTrue(any("새로운 최고 점수" in line for line in io.output))

    def test_play_quiz_handles_empty_quiz_list(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            io = ScriptedIO([])
            game = QuizGame(
                Console(io.input, io.print),
                StateRepository(Path(directory) / "state.json"),
            )
            game.quizzes.clear()

            game.play_quiz()

            self.assertTrue(any("등록된 퀴즈가 없습니다" in line for line in io.output))


class QuizAddTests(unittest.TestCase):
    def test_add_quiz_validates_and_persists_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            repository = StateRepository(state_path)
            io = ScriptedIO(
                [
                    "  JSON은 무엇의 약자인가?  ",
                    "Java Source Object Network",
                    "JavaScript Object Notation",
                    "Joined Standard Object Name",
                    "Java Syntax Or Number",
                    "abc",
                    "5",
                    "2",
                    "웹 데이터 교환 형식",
                ]
            )
            game = QuizGame(Console(io.input, io.print), repository)

            game.add_quiz()

            self.assertEqual(len(game.quizzes), 8)
            self.assertEqual(game.quizzes[-1].answer, 2)
            self.assertTrue(state_path.exists())
            reloaded = StateRepository(state_path).load()
            self.assertEqual(reloaded.quizzes[-1].question, "JSON은 무엇의 약자인가?")
            self.assertTrue(any("숫자로 입력" in line for line in io.output))
            self.assertTrue(any("1부터 4 사이" in line for line in io.output))

    def test_add_quiz_rejects_duplicate_question(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = StateRepository(Path(directory) / "state.json")
            game = QuizGame(repository=repository)
            existing = game.quizzes[0].question
            io = ScriptedIO([existing])
            game.console = Console(io.input, io.print)

            game.add_quiz()

            self.assertEqual(len(game.quizzes), 7)
            self.assertTrue(any("이미 등록" in line for line in io.output))


class QuizListTests(unittest.TestCase):
    def test_list_quizzes_prints_questions_choices_and_answers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            io = ScriptedIO([])
            game = QuizGame(
                Console(io.input, io.print),
                StateRepository(Path(directory) / "state.json"),
            )

            game.list_quizzes()

            rendered = "\n".join(io.output)
            self.assertIn("퀴즈 목록 (7개)", rendered)
            self.assertIn("Q1.", rendered)
            self.assertIn("정답:", rendered)
            self.assertIn("힌트:", rendered)

    def test_list_quizzes_handles_empty_list(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            io = ScriptedIO([])
            game = QuizGame(
                Console(io.input, io.print),
                StateRepository(Path(directory) / "state.json"),
            )
            game.quizzes.clear()

            game.list_quizzes()

            self.assertIn("저장된 퀴즈가 없습니다.", io.output)


if __name__ == "__main__":
    unittest.main()
