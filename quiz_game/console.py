"""Reusable console input and output helpers."""

from __future__ import annotations

from collections.abc import Callable


class InputAborted(Exception):
    """Raised when the user interrupts input with Ctrl+C or EOF."""


class Console:
    """Validate console input and keep user-facing messages consistent."""

    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ) -> None:
        self._input = input_func
        self._output = output_func

    def write(self, message: str = "") -> None:
        """Write one line to the console."""
        self._output(message)

    def read_text(self, prompt: str, *, allow_empty: bool = False) -> str:
        """Read trimmed text, retrying when an empty value is not allowed."""
        while True:
            try:
                value = self._input(prompt).strip()
            except (KeyboardInterrupt, EOFError) as error:
                raise InputAborted from error

            if value or allow_empty:
                return value
            self.write("빈 값은 입력할 수 없습니다. 다시 입력해 주세요.")

    def read_int(self, prompt: str, minimum: int, maximum: int) -> int:
        """Read an integer inside the inclusive range."""
        while True:
            raw_value = self.read_text(prompt)
            try:
                value = int(raw_value)
            except ValueError:
                self.write("숫자로 입력해 주세요.")
                continue

            if minimum <= value <= maximum:
                return value

            self.write(f"{minimum}부터 {maximum} 사이의 번호를 입력해 주세요.")


