# E1-2 Python 퀴즈 게임

## 프로젝트 개요

Python 기본 문법과 클래스, JSON 파일 저장을 연습하기 위한 콘솔 퀴즈 게임입니다.
코드는 설명하기 쉽도록 `main.py` 하나에 `Quiz`와 `QuizGame` 두 클래스만 사용했습니다.

## 퀴즈 주제와 선정 이유

주제는 Python 기초입니다.
프로그램을 만들면서 사용한 `list`, `dict`, 조건문, 함수, 예외 처리를 문제로 다시 복습하기 위해 선택했습니다.
기본 문제는 5개입니다.

## 실행 환경

- Python 3.10 이상
- 외부 라이브러리 없음
- Windows, macOS, Linux에서 실행 가능

## 실행 방법

```bash
git clone https://github.com/juhyulee/E1-2.git
cd E1-2
python main.py
```

macOS:

```bash
python3 main.py
```

## 메뉴와 기능

```text
=== Python 퀴즈 게임 ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
```

- 퀴즈 풀기: 저장된 문제를 순서대로 풀고 100점 기준으로 점수를 계산합니다.
- 퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력하고 즉시 저장합니다.
- 퀴즈 목록: 등록된 문제 제목을 출력합니다.
- 점수 확인: 지금까지의 최고 점수를 출력합니다.
- 종료: 현재 퀴즈와 최고 점수를 저장합니다.

빈 입력, 문자가 들어간 숫자 입력, 범위를 벗어난 숫자는 다시 입력받습니다.
`Ctrl+C` 또는 입력 종료가 발생하면 가능한 데이터를 저장한 뒤 안전하게 종료합니다.

## 파일 구조

```text
E1-2/
├── main.py
├── state.json
├── README.md
├── .gitignore
└── evidence/logs/git-workflow.txt
```

핵심 코드는 `main.py` 하나입니다.

## 클래스 설명

### Quiz

퀴즈 한 문제를 나타냅니다.

- 속성: `question`, `choices`, `answer`
- `show()`: 문제와 선택지 출력
- `is_correct()`: 사용자의 정답 확인
- `to_dict()`: JSON 저장용 딕셔너리 변환

### QuizGame

게임 전체를 관리합니다.

- 퀴즈 목록과 최고 점수 보관
- 메뉴 실행
- 퀴즈 풀기·추가·목록·점수 기능
- `state.json` 저장과 불러오기
- 숫자와 빈 입력 검증

## state.json

위치: 프로젝트 루트의 `state.json`

```json
{
  "quizzes": [
    {
      "question": "Python에서 여러 값을 순서대로 저장하는 자료형은?",
      "choices": ["int", "list", "bool", "str"],
      "answer": 2
    }
  ],
  "best_score": null
}
```

- `quizzes`: 문제 목록
- `question`: 문제 내용
- `choices`: 선택지 4개
- `answer`: 정답 번호 1~4
- `best_score`: 최고 점수. 아직 풀지 않았다면 `null`

파일은 UTF-8로 읽고 씁니다.
파일이 없거나 손상되면 기본 퀴즈 5개로 시작합니다.

## 프로그램 흐름

```text
프로그램 시작
  → state.json 불러오기
  → 메뉴 번호 입력
  → 선택한 기능 실행
  → 변경 내용 저장
  → 종료
```

## Python 개념 설명

### 변수와 자료형

- 변수: 값을 이름으로 저장해 다시 사용하기 위한 공간
- `int`: 정답 번호와 점수 같은 정수
- `str`: 문제와 선택지 같은 문자열
- `bool`: 정답인지 아닌지 나타내는 참·거짓
- `list`: 여러 퀴즈와 선택지를 순서대로 저장
- `dict`: JSON에 저장할 키와 값의 묶음

### 조건문과 반복문

- `if/elif/else`: 메뉴 번호나 정답 여부에 따라 다른 코드를 실행합니다.
- `for`: 퀴즈와 선택지처럼 개수가 정해진 목록을 순회합니다.
- `while`: 메뉴와 잘못된 입력을 계속 반복합니다.

### 클래스와 객체

- 클래스: 관련 데이터와 기능을 묶은 설계도
- 객체: 클래스로 실제 생성한 값
- `__init__`: 객체를 만들 때 속성을 초기화하는 메서드
- `self`: 현재 객체 자신

### JSON과 예외 처리

JSON은 `dict`와 `list` 형태의 데이터를 텍스트 파일로 저장하기 좋습니다.
`try/except`를 사용해 파일 없음, JSON 손상, 입력 중단 오류를 처리합니다.

## Git 작업 조건

기존 저장소에는 10개 이상의 기능 단위 커밋과 `feature/quiz-play` 브랜치 병합 기록이 있습니다.

```bash
git log --oneline --graph --all
```

`clone → 수정 → commit → push → 기존 폴더에서 pull` 실습 기록:

[Git 워크플로 로그](evidence/logs/git-workflow.txt)

| 명령 | 역할 |
|---|---|
| `git init` | 로컬 저장소 생성 |
| `git add` | 커밋할 변경 선택 |
| `git commit` | 변경 이력 저장 |
| `git push` | 로컬 커밋을 GitHub에 전송 |
| `git pull` | 원격 변경을 가져오기 |
| `git checkout` | 브랜치 생성 또는 전환 |
| `git clone` | 원격 저장소 복제 |

Git은 로컬 버전 관리 도구이고 GitHub는 원격 저장소와 협업 서비스입니다.

## 평가 때 설명할 핵심

1. `Quiz`는 문제 하나, `QuizGame`은 게임 전체를 담당합니다.
2. 메뉴는 `while`, 문제와 선택지는 `for`로 반복합니다.
3. `if/elif/else`로 메뉴 기능과 정답을 구분합니다.
4. 퀴즈와 최고 점수를 `state.json`에 저장해 재실행 후에도 유지합니다.
5. 파일이나 입력 오류는 `try/except`로 처리합니다.

## 보너스 기능 제외

설명을 단순하게 유지하기 위해 랜덤 출제, 문제 수 선택, 힌트, 삭제, 점수 히스토리는 구현하지 않았습니다.

## 보안

토큰, 비밀번호, 개인키는 저장하지 않습니다. 화면을 캡처할 때도 인증 정보를 포함하지 않습니다.
