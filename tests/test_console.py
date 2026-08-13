from __future__ import annotations

import unittest

from quiz_game.console import Console, InputAborted


class ConsoleInputTests(unittest.TestCase):
    def test_read_int_retries_empty_text_non_number_and_out_of_range(self) -> None:
        answers = iter(["   ", "abc", "9", " 2 "])
        output: list[str] = []
        console = Console(lambda _: next(answers), output.append)

        result = console.read_int("번호: ", 1, 5)

        self.assertEqual(result, 2)
        self.assertTrue(any("빈 값" in message for message in output))
        self.assertTrue(any("숫자로" in message for message in output))
        self.assertTrue(any("1부터 5" in message for message in output))

    def test_read_text_converts_keyboard_interrupt_to_input_aborted(self) -> None:
        def interrupt(_: str) -> str:
            raise KeyboardInterrupt

        console = Console(interrupt, lambda _: None)
        with self.assertRaises(InputAborted):
            console.read_text("입력: ")

    def test_read_text_converts_eof_to_input_aborted(self) -> None:
        def end_of_input(_: str) -> str:
            raise EOFError

        console = Console(end_of_input, lambda _: None)
        with self.assertRaises(InputAborted):
            console.read_text("입력: ")


if __name__ == "__main__":
    unittest.main()

