"""Main menu and application orchestration."""

from __future__ import annotations

import random
from datetime import datetime

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
        """Play a randomized quiz session and persist its result."""
        if not self.quizzes:
            self.console.write("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        self.console.write(f"\n현재 퀴즈는 {len(self.quizzes)}개입니다.")
        question_count = self.console.read_int(
            f"몇 문제를 풀까요? (1~{len(self.quizzes)}): ",
            1,
            len(self.quizzes),
        )
        selected_quizzes = random.sample(self.quizzes, question_count)
        correct_count = 0

        for number, quiz in enumerate(selected_quizzes, start=1):
            self.console.write(f"\n{quiz.format_question(number)}")
            selected_answer = self.console.read_int("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(selected_answer):
                correct_count += 1
                self.console.write("정답입니다! ✅")
            else:
                self.console.write(
                    f"오답입니다. 정답은 {quiz.answer}번 "
                    f"'{quiz.correct_choice}'입니다."
                )

        self.console.write(
            f"\n결과: {question_count}문제 중 {correct_count}문제 정답 "
            f"({correct_count / question_count:.0%})"
        )
        self._record_score(correct_count, question_count)
        self.repository.save(self.state)

    def _record_score(self, score: int, total: int) -> None:
        """Append score history and update the best result when needed."""
        self.state.score_history.append(
            {
                "played_at": datetime.now().isoformat(timespec="seconds"),
                "score": score,
                "total": total,
            }
        )

        previous_ratio = (
            self.state.best_score / self.state.best_total
            if self.state.best_total
            else -1.0
        )
        current_ratio = score / total
        is_better = current_ratio > previous_ratio or (
            current_ratio == previous_ratio and score > self.state.best_score
        )
        if is_better:
            self.state.best_score = score
            self.state.best_total = total
            self.console.write("새로운 최고 점수입니다! 🏆")

    def add_quiz(self) -> None:
        """Register, validate, and immediately save a new quiz."""
        self.console.write("\n=== 새 퀴즈 추가 ===")
        question = self.console.read_text("문제: ")

        if any(quiz.question == question for quiz in self.quizzes):
            self.console.write("같은 문제가 이미 등록되어 있습니다.")
            return

        choices = [
            self.console.read_text(f"선택지 {number}: ")
            for number in range(1, 5)
        ]
        answer = self.console.read_int("정답 번호 (1~4): ", 1, 4)
        hint = self.console.read_text(
            "힌트 (없으면 Enter): ",
            allow_empty=True,
        )

        quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.quizzes.append(quiz)
        self.state.quizzes = self.quizzes

        if self.repository.save(self.state):
            self.console.write(f"퀴즈가 등록되었습니다. (총 {len(self.quizzes)}개)")
        else:
            self.quizzes.pop()
            self.console.write(self.repository.last_message)

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
