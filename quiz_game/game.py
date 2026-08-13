"""Main menu and application orchestration."""

from __future__ import annotations

from quiz_game.console import Console, InputAborted
from quiz_game.models import Quiz
from quiz_game.storage import GameState, StateRepository


class QuizGame:
    """Coordinate the quiz game's menu and features."""

    MENU = (
        "1. 퀴즈 풀기",
        "2. 퀴즈 추가",
        "3. 퀴즈 목록",
        "4. 최고 점수 확인",
        "5. 종료",
    )

    def __init__(
        self,
        console: Console | None = None,
        repository: StateRepository | None = None,
    ) -> None:
        self.console = console or Console()
        self.repository = repository or StateRepository()
        self.state: GameState = self.repository.load()
        self.quizzes: list[Quiz] = self.state.quizzes
        self.running = True

    def show_menu(self) -> None:
        """Display all menu choices."""
        self.console.write("\n=== Python Console Quiz Game ===")
        for item in self.MENU:
            self.console.write(item)

    def run(self) -> None:
        """Run the menu loop until the user chooses to exit."""
        if self.repository.last_message:
            self.console.write(self.repository.last_message)
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
        if selection == 1:
            self.play_quiz()
        elif selection == 2:
            self.add_quiz()
        elif selection == 3:
            self.list_quizzes()
        elif selection == 4:
            self.show_best_score()
        elif selection == 5:
            self.running = False

    def play_quiz(self) -> None:
        """Play a quiz session. Implemented on the feature branch."""
        self.console.write("[퀴즈 풀기] 기능을 준비 중입니다.")

    def add_quiz(self) -> None:
        """Register a new quiz. Implemented in a later feature commit."""
        self.console.write("[퀴즈 추가] 기능을 준비 중입니다.")

    def list_quizzes(self) -> None:
        """List saved quizzes. Implemented in a later feature commit."""
        self.console.write("[퀴즈 목록] 기능을 준비 중입니다.")

    def show_best_score(self) -> None:
        """Show the highest score. Implemented in a later feature commit."""
        self.console.write("[최고 점수] 기능을 준비 중입니다.")

    def shutdown(self) -> None:
        """Save the latest state before the program exits."""
        self.state.quizzes = self.quizzes
        if not self.repository.save(self.state):
            self.console.write(self.repository.last_message)
        self.console.write("게임을 종료합니다. 이용해 주셔서 감사합니다!")

