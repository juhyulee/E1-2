"""Main menu and application orchestration."""

from __future__ import annotations

from quiz_game.console import Console, InputAborted


class QuizGame:
    """Coordinate the quiz game's menu and features."""

    MENU = (
        "1. 퀴즈 풀기",
        "2. 퀴즈 추가",
        "3. 퀴즈 목록",
        "4. 최고 점수 확인",
        "5. 종료",
    )

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self.running = True

    def show_menu(self) -> None:
        """Display all menu choices."""
        self.console.write("\n=== Python Console Quiz Game ===")
        for item in self.MENU:
            self.console.write(item)

    def run(self) -> None:
        """Run the menu loop until the user chooses to exit."""
        try:
            while self.running:
                self.show_menu()
                selection = self.console.read_int("메뉴 선택: ", 1, len(self.MENU))
                self.handle_menu(selection)
        except InputAborted:
            self.console.write("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        finally:
            self.shutdown()

    def handle_menu(self, selection: int) -> None:
        """Dispatch one validated menu choice."""
        if selection == 5:
            self.running = False
            return

        feature_names = {
            1: "퀴즈 풀기",
            2: "퀴즈 추가",
            3: "퀴즈 목록",
            4: "최고 점수 확인",
        }
        self.console.write(f"[{feature_names[selection]}] 기능을 준비 중입니다.")

    def shutdown(self) -> None:
        """Perform final cleanup before the program exits."""
        self.console.write("게임을 종료합니다. 이용해 주셔서 감사합니다!")


