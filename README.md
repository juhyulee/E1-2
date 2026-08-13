# Python Console Quiz Game

## 프로젝트 개요

Python 기본 문법, 객체 지향 설계, UTF-8 JSON 영속성, Git 브랜치 협업 흐름을 하나의 동작하는 콘솔 프로그램으로 구현한 프로젝트입니다.

프로그램을 실행하면 메뉴에서 퀴즈 풀기·추가·목록·최고 점수 확인·종료를 선택할 수 있습니다. 사용자가 등록한 퀴즈와 점수 기록은 프로젝트 루트의 `state.json`에 저장되어 프로그램을 다시 실행해도 유지됩니다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초**입니다.

이 프로젝트를 실행하는 데 사용한 언어 자체를 퀴즈로 복습하면 `list`, `dict`, 조건문, 함수, 클래스, 예외 처리 같은 개념을 코드와 문제 양쪽에서 반복해서 확인할 수 있기 때문입니다. 직접 작성한 기본 문제 7개가 포함되어 있으며 요구 수량인 5개 이상을 충족합니다.

## 실행 환경

- Python 3.12.13에서 개발·검증
- Python 3.11 이상 권장
- 외부 패키지 없음: Python 표준 라이브러리만 사용
- Windows PowerShell, macOS Terminal, Linux shell에서 실행 가능

## 실행 방법

```bash
git clone https://github.com/juhyulee/E1-2.git
cd E1-2
python main.py
```

Windows에서 `python` 명령 대신 Python Launcher를 사용한다면 다음과 같이 실행합니다.

```powershell
py main.py
```

실행 메뉴:

```text
=== Python Console Quiz Game ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 최고 점수 확인
5. 종료
메뉴 선택:
```

[실제 전체 실행 로그](evidence/logs/sample-session.txt)에서 빈 입력, 문자 입력, 범위 초과, 퀴즈 풀이, 점수 확인, 종료 흐름을 확인할 수 있습니다.

## 기능 목록

### 메뉴와 안전한 입력

- 입력 앞뒤 공백 제거
- 빈 입력 시 안내 후 재입력
- `abc`처럼 정수로 변환할 수 없는 입력 처리
- 메뉴 `9`, 정답 `0`처럼 허용 범위 밖 입력 처리
- `Ctrl+C`(`KeyboardInterrupt`)와 입력 종료(`EOFError`) 시 현재 데이터를 저장하고 정상 종료

### 퀴즈 풀기

- 저장된 퀴즈에서 무작위 출제
- 풀 문제 수 선택
- 선택지 4개와 정답 번호 검증
- 문제마다 정답·오답 및 실제 정답 표시
- 세션 종료 후 정답 개수와 정답률 출력

### 퀴즈 추가

- 문제, 선택지 4개, 정답 번호, 선택적 힌트 입력
- 중복 문제 차단
- 잘못된 정답 번호 재입력
- 등록 즉시 `state.json` 저장

### 퀴즈 목록

- 저장된 모든 문제와 선택지 확인
- 정답과 힌트 확인
- 퀴즈가 없을 때 안내

### 점수와 기록

- 최고 점수와 정답률 표시
- 최근 게임 기록 최대 5개 표시
- 모든 게임 기록의 날짜·점수·문제 수를 JSON에 저장
- 문제 수가 다를 때는 정답률을 먼저 비교하고, 정답률이 같으면 더 많은 정답을 기록한 결과를 최고 점수로 선택
- 아직 플레이하지 않았을 때 별도 안내

### 데이터 복구

- `state.json`이 없으면 기본 퀴즈 7개 사용
- JSON이 손상되거나 스키마가 잘못되면 기본 데이터로 복구
- 손상 파일은 `state.json.corrupt-YYYYMMDD-HHMMSS` 이름으로 보존
- 임시 파일에 먼저 쓴 뒤 교체하는 방식으로 저장 중 중단 위험 완화

## 파일 구조

```text
E1-2/
├── main.py                     # 프로그램 진입점
├── state.json                  # 퀴즈·최고 점수·게임 기록 영속 데이터
├── quiz_game/
│   ├── __init__.py
│   ├── console.py              # 공통 입력 검증과 인터럽트 처리
│   ├── defaults.py             # Python 기초 기본 퀴즈 7개
│   ├── game.py                 # QuizGame 메뉴와 전체 게임 흐름
│   ├── models.py               # Quiz 클래스와 JSON 변환
│   └── storage.py              # GameState와 StateRepository
├── tests/
│   ├── test_console.py         # 입력 오류·Ctrl+C·EOF 테스트
│   ├── test_game.py            # 풀이·추가·목록·점수 테스트
│   └── test_storage.py         # 파일 없음·손상·UTF-8 왕복 테스트
├── evidence/logs/              # 실행·테스트·Git 실습 증거
├── .gitignore
├── .gitattributes
└── README.md
```

## 클래스 구조

### `Quiz`

개별 문제를 표현합니다.

- 속성: `question`, `choices`, `answer`, `hint`
- `__post_init__`: 문제·선택지·정답 범위 검증
- `format_question`: 문제와 4개 선택지를 출력 형식으로 변환
- `is_correct`: 선택한 답과 정답 비교
- `to_dict` / `from_dict`: 객체와 JSON용 `dict` 사이 변환

### `QuizGame`

프로그램 전체 흐름을 관리합니다.

- 속성: `quizzes`, `state`, `repository`, `console`, `running`
- 메서드: 메뉴 표시, 기능 분기, 퀴즈 풀이, 추가, 목록, 점수 표시, 안전 종료
- 기능별 메서드를 분리해 메뉴 코드와 도메인 동작이 섞이지 않도록 구성

### `StateRepository`

파일 입출력만 담당합니다.

- UTF-8 JSON 읽기·쓰기
- 데이터 스키마 검증
- 파일 없음·손상·I/O 오류 처리
- 임시 파일을 이용한 원자적 저장

`Console`, `GameState`까지 역할별 객체로 나누어 입력, 게임 규칙, 데이터 저장을 독립적으로 테스트할 수 있게 했습니다.

## `state.json` 설명

위치: **프로젝트 루트의 `state.json`**

```json
{
  "quizzes": [
    {
      "question": "함수를 정의할 때 사용하는 Python 키워드는?",
      "choices": ["def", "func", "function", "return"],
      "answer": 1,
      "hint": "define의 앞 세 글자입니다."
    }
  ],
  "best_score": 1,
  "best_total": 1,
  "score_history": [
    {
      "played_at": "2026-08-13T12:00:00",
      "score": 1,
      "total": 1
    }
  ]
}
```

- `quizzes`: 퀴즈 객체 목록
- `best_score`: 최고 기록의 정답 개수
- `best_total`: 최고 기록에서 출제된 문제 수
- `score_history`: 모든 게임의 실행 시각·정답 개수·문제 수
- `ensure_ascii=False`와 `encoding="utf-8"`을 사용해 한글을 그대로 저장

## 핵심 실행 흐름

```text
main.py
  → QuizGame 생성
  → StateRepository.load()
  → state.json 또는 기본 퀴즈 로드
  → while 메뉴 반복
  → 선택한 기능 메서드 실행
  → 변경 시 StateRepository.save()
  → 종료 또는 인터럽트 시 최종 저장
```

## 입력과 예외 처리 예시

```text
메뉴 선택:
빈 값은 입력할 수 없습니다. 다시 입력해 주세요.
메뉴 선택: abc
숫자로 입력해 주세요.
메뉴 선택: 9
1부터 5 사이의 번호를 입력해 주세요.
```

`Console.read_int()`가 이 로직을 공통 처리하므로 메뉴, 문제 수, 정답 번호가 같은 규칙을 사용합니다.

## 테스트

```bash
python -m unittest -v
python -m compileall -q main.py quiz_game tests
```

검증 결과:

- 자동 테스트 14개 통과
- 문법 컴파일 검사 성공
- 파일 없음·손상 JSON·한글 UTF-8 왕복 검증
- 숫자 변환 실패·빈 입력·범위 초과 검증
- `KeyboardInterrupt`·`EOFError` 변환 검증
- 퀴즈 풀이·추가·목록·점수 기록 검증

실제 결과는 [테스트 로그](evidence/logs/test-results.txt)와 [최종 요구사항 검증 로그](evidence/logs/final-verification.txt)에 있습니다.

## Git 작업 이력

기능별로 커밋했으며 10개 이상의 의미 있는 커밋이 존재합니다.

```bash
git log --graph --oneline --decorate --all
```

주요 흐름:

1. 프로젝트 구조 및 `.gitignore` 생성
2. 메뉴와 입력 검증
3. `Quiz` 클래스
4. 기본 퀴즈 7개
5. UTF-8 JSON 영속성
6. `QuizGame`과 저장 상태 연결
7. `feature/quiz-play` 브랜치에서 퀴즈 풀이 구현
8. `git merge --no-ff feature/quiz-play`로 `main` 병합
9. 퀴즈 추가
10. 퀴즈 목록
11. 최고 점수와 기록
12. 예외·파일 복구 테스트
13. Windows 콘솔 호환성 수정

브랜치/병합 그래프에서 `feature/quiz-play` 커밋과 merge 커밋을 확인할 수 있습니다. 개발 완료 후 별도 디렉터리로 다시 `clone`하고, 복제본에서 README를 수정해 `commit → push`한 다음 최초 작업 폴더에서 `pull`하는 실습도 수행했습니다. 상세 명령과 출력은 [Git 워크플로 로그](evidence/logs/git-workflow.txt)에 기록합니다.

## Python 개념 정리

### 변수와 자료형

변수는 값을 이름으로 저장해 다시 사용하고 의미를 전달합니다.

- `int`: 정수. 예: 정답 번호, 점수
- `str`: 문자열. 예: 문제와 선택지
- `bool`: 참/거짓. 예: 정답 여부, 게임 실행 여부
- `list`: 순서가 있는 값 목록. 예: 퀴즈·선택지·기록 목록
- `dict`: 키와 값의 관계. 예: JSON으로 저장할 퀴즈와 점수

### 조건문과 반복문

- `if/elif/else`: 메뉴 선택, 정답 여부, 최고 점수 갱신처럼 조건에 따라 다른 동작을 수행
- `for`: 퀴즈나 선택지처럼 개수가 정해진 컬렉션 순회
- `while`: 사용자가 종료를 선택할 때까지 메뉴를 반복하거나 올바른 입력을 받을 때까지 재시도

### 함수

함수는 반복되는 작업에 이름을 붙입니다. 매개변수는 함수가 받을 입력이고, 반환값은 처리 후 돌려주는 결과입니다. 예를 들어 `is_correct(selected_answer)`는 선택 번호를 매개변수로 받고 `bool`을 반환합니다.

### 클래스와 객체

클래스는 관련 데이터와 동작을 묶은 설계도이고, 객체는 그 설계도로 만든 실제 값입니다. `Quiz` 클래스 하나로 서로 다른 7개의 문제 객체를 만들 수 있습니다.

- `__init__`: 객체 생성 시 속성을 초기화
- `self`: 현재 객체 자체를 가리킴
- 속성: 객체가 가진 데이터
- 메서드: 객체가 수행하는 동작

### JSON과 파일 입출력

JSON은 문자열, 숫자, 배열, 객체처럼 언어에 독립적인 구조로 데이터를 표현하는 텍스트 형식입니다. 사람이 읽기 쉽고 Python의 `dict`/`list`와 자연스럽게 변환되어 작은 프로그램의 영속 데이터 저장에 적합합니다.

```python
with path.open("r", encoding="utf-8") as file:
    data = json.load(file)
```

읽기·쓰기 코드는 `try/except`로 감싸 파일 없음, 손상된 JSON, 권한 문제 때문에 프로그램 전체가 비정상 종료되지 않도록 했습니다.

## Git 명령 설명

| 명령 | 역할 |
|---|---|
| `git init` | 현재 폴더에 새 로컬 Git 저장소 생성 |
| `git add` | 다음 커밋에 포함할 변경을 스테이징 |
| `git commit` | 스테이징된 변경을 하나의 이력으로 기록 |
| `git push` | 로컬 커밋을 GitHub 원격 저장소에 전송 |
| `git pull` | 원격 변경을 가져와 현재 브랜치에 통합 |
| `git checkout` | 브랜치를 전환하거나 새 브랜치를 생성 |
| `git clone` | 원격 저장소 전체를 새 로컬 폴더로 복제 |
| `git merge` | 다른 브랜치의 작업을 현재 브랜치에 병합 |

Git은 로컬 변경 이력을 관리하는 도구이고, GitHub는 Git 저장소를 원격에서 공유하고 협업하는 플랫폼입니다.

## 트러블슈팅

### Windows PowerShell에서 이모지 출력 실패

- **문제:** 실제 시연 중 정답 표시 이모지에서 `UnicodeEncodeError` 발생
- **원인:** Windows PowerShell 5.1의 기본 CP949 코드 페이지가 일부 이모지를 표현하지 못함
- **확인:** 14개 로직 테스트는 통과했지만 실제 콘솔 전체 실행에서 오류 재현
- **해결:** 이모지를 `[OK]`, `[BEST]`처럼 모든 콘솔에서 표시 가능한 텍스트로 교체
- **결과:** 동일한 실제 세션이 정상 종료되고 점수까지 저장됨

### 손상된 JSON 데이터

- **문제:** 사용자가 `state.json`을 잘못 편집하면 `json.load()` 실패 가능
- **확인:** 테스트에서 의도적으로 `{not valid json` 파일을 생성
- **해결:** `JSONDecodeError`를 처리해 손상 파일을 별도 백업하고 기본 퀴즈로 복구
- **결과:** 프로그램이 중단되지 않고 7개 기본 퀴즈로 실행됨

### PowerShell의 native stderr 표시

- **문제:** `unittest -v`의 정상 진행 메시지가 stderr에 기록되어 PowerShell 로그에 오류 메타데이터가 섞임
- **원인:** `unittest`는 상세 진행 출력을 stderr로 보내고 Windows PowerShell 5.1은 native stderr를 오류 레코드로 래핑함
- **해결:** `cmd.exe`에서 stdout/stderr를 병합하고 실제 프로세스 종료 코드가 `0`인지 확인
- **결과:** 오류 메타데이터 없는 테스트 로그와 `unittest exit code: 0` 확보

## 보안과 개인정보

- 비밀번호, 토큰, 개인키, 인증 코드를 저장하지 않습니다.
- Git 작성자 이메일은 GitHub noreply 주소를 사용합니다.
- 상태 파일에는 퀴즈와 점수만 저장합니다.
- Python 캐시, 가상환경, 임시 파일, 손상 파일 백업은 `.gitignore`에서 제외합니다.

---

Clone/pull 실습 완료: 별도 clone 디렉터리에서 이 문장을 추가하고 `commit → push`한 뒤, 최초 작업 디렉터리에서 `git pull`로 가져왔습니다.
