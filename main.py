import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"

DEFAULT_QUIZZES = [
    {
        "question": "Python에서 여러 값을 순서대로 저장하는 자료형은?",
        "choices": ["int", "list", "bool", "str"],
        "answer": 2
    },
    {
        "question": "조건에 따라 코드를 실행할 때 사용하는 키워드는?",
        "choices": ["if", "for", "def", "import"],
        "answer": 1
    },
    {
        "question": "함수를 정의할 때 사용하는 키워드는?",
        "choices": ["class", "return", "def", "while"],
        "answer": 3
    },
    {
        "question": "키와 값으로 데이터를 저장하는 자료형은?",
        "choices": ["list", "dict", "tuple", "str"],
        "answer": 2
    },
    {
        "question": "예외 처리를 시작할 때 사용하는 키워드는?",
        "choices": ["try", "with", "match", "yield"],
        "answer": 1
    }
]


class Quiz:
    """퀴즈 한 문제를 저장하고 채점하는 클래스."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number):
        print("\n[문제 {}] {}".format(number, self.question))
        for index, choice in enumerate(self.choices, start=1):
            print("{}. {}".format(index, choice))

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }


class QuizGame:
    """메뉴, 퀴즈, 점수, JSON 저장을 관리하는 클래스."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load()

    def load(self):
        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            loaded = []
            for item in data["quizzes"]:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if not isinstance(question, str) or not question.strip():
                    raise ValueError("잘못된 문제")
                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError("선택지는 4개여야 함")
                if not isinstance(answer, int) or answer not in range(1, 5):
                    raise ValueError("정답은 1~4")

                loaded.append(Quiz(question, choices, answer))

            self.quizzes = loaded
            best_score = data.get("best_score")
            self.best_score = best_score if isinstance(best_score, int) else None
            print("저장된 데이터를 불러왔습니다.")
        except FileNotFoundError:
            print("state.json이 없어 기본 퀴즈로 시작합니다.")
            self.use_default_quizzes()
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("state.json이 손상되어 기본 퀴즈로 복구합니다.")
            self.use_default_quizzes()

    def use_default_quizzes(self):
        self.quizzes = [
            Quiz(item["question"], item["choices"], item["answer"])
            for item in DEFAULT_QUIZZES
        ]
        self.best_score = None

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with STATE_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print("저장 오류:", error)

    def input_number(self, prompt, minimum, maximum):
        while True:
            text = input(prompt).strip()

            if not text:
                print("빈 값은 입력할 수 없습니다.")
                continue

            try:
                number = int(text)
            except ValueError:
                print("숫자를 입력하세요.")
                continue

            if minimum <= number <= maximum:
                return number

            print("{}부터 {} 사이의 숫자를 입력하세요.".format(minimum, maximum))

    def input_text(self, prompt):
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("빈 값은 입력할 수 없습니다.")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct = 0
        print("\n총 {}문제를 시작합니다.".format(len(self.quizzes)))

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.show(number)
            answer = self.input_number("정답 번호 (1~4): ", 1, 4)

            if quiz.is_correct(answer):
                print("정답입니다.")
                correct += 1
            else:
                print("오답입니다. 정답은 {}번입니다.".format(quiz.answer))

        score = round(correct / len(self.quizzes) * 100)
        print("\n결과: {}문제 중 {}문제 정답, {}점".format(
            len(self.quizzes), correct, score
        ))

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다.")

        self.save()

    def add_quiz(self):
        print("\n새 퀴즈를 추가합니다.")
        question = self.input_text("문제: ")
        choices = []

        for number in range(1, 5):
            choices.append(self.input_text("선택지 {}: ".format(number)))

        answer = self.input_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("퀴즈가 추가되었습니다.")

    def show_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n등록된 퀴즈: {}개".format(len(self.quizzes)))
        for number, quiz in enumerate(self.quizzes, start=1):
            print("{}. {}".format(number, quiz.question))

    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print("최고 점수: {}점".format(self.best_score))

    def run(self):
        while True:
            print("\n=== Python 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")

            choice = self.input_number("선택: ", 1, 5)

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            else:
                self.save()
                print("게임을 종료합니다.")
                break


if __name__ == "__main__":
    game = QuizGame()

    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 저장 후 종료합니다.")
        game.save()
