# Screen Definition Generator

PRD(Product Requirements Document)를 넣으면 Claude Code가 화면정의서를 자동 생성합니다.

별도 API 키 없이, Claude Code만 있으면 됩니다.

## 사용 방법

### 1. 프로젝트 클론

```bash
git clone https://github.com/zoe765/screen-def-generator.git
cd screen-def-generator
```

### 2. PRD 파일 넣기

`input/` 폴더에 PRD 파일을 넣습니다. 지원 형식: `.md`, `.txt`, `.docx`

```bash
cp my-prd.md input/
```

> `.docx` 파일은 자동으로 텍스트 추출됩니다 (macOS `textutil` 사용).
> 수동 변환이 필요하면: `bash scripts/convert_docx.sh`

### 3. Claude Code 실행

```bash
claude
```

실행 후 다음과 같이 입력합니다:

```
화면정의서를 생성해줘
```

Claude Code가 CLAUDE.md의 워크플로우를 따라 자동으로 진행합니다:

1. PRD 읽기 및 분석
2. 사전 인터뷰 (프로젝트 정보, 화면 목록, 디자인 방향 확인)
3. 화면 목록 확정 (사용자 승인)
4. 화면별 정의서 생성
5. 품질 검증 및 저장
6. 내보내기 (선택 — HTML / Google Docs)

## 출력 결과물

`output/` 폴더에 생성됩니다:

```
output/
├── 00_화면목록.md          # 전체 화면 인덱스 + 흐름도
├── 01_스플래시.md          # 각 화면별 정의서
├── 02_온보딩.md
├── 03_로그인.md
└── ...
```

각 화면정의서는 10개 섹션으로 구성됩니다:

| # | 섹션 | 설명 |
|---|------|------|
| 1 | User Goal | 사용자 관점 목표 |
| 2 | System Goal | 비즈니스 관점 목표 |
| 3 | Data Model | 데이터 구조와 흐름 |
| 4 | Information Hierarchy | 정보의 시각적 우선순위 |
| 5 | Actions | 사용자가 할 수 있는 행동 |
| 6 | Input & Validation | 입력과 검증 규칙 |
| 7 | Navigation & Flow | 화면 전환과 상태 |
| 8 | Edge Cases & Error | 예외와 오류 처리 |
| 9 | Emotional Direction | 감정 톤과 UX 라이팅 |
| 10 | Constraints | 기술/비즈니스 제약 |

## Google Docs로 내보내기

화면정의서를 Google Docs에 옮기고 싶다면 HTML 변환 스크립트를 사용합니다:

```bash
python3 scripts/convert_to_html.py --open
```

브라우저에서 열린 HTML을 `Cmd+A` → `Cmd+C` → Google Docs에서 `Cmd+V` 하면 표와 스타일이 유지된 채 복사됩니다.

옵션:

```bash
# 프로젝트명 지정
python3 scripts/convert_to_html.py --project "내 프로젝트"

# 출력 경로 지정
python3 scripts/convert_to_html.py --output ~/Desktop/output.html

# 다른 폴더의 MD 파일 변환
python3 scripts/convert_to_html.py --input-dir /path/to/md-files
```

## 커스터마이징

### 템플릿 구조 변경

`templates/screen_template.md`를 수정하면 생성되는 화면정의서의 구조가 바뀝니다.

### 품질 기준 변경

`templates/screen_example.md`의 예시를 교체하면 생성 품질의 기준이 바뀝니다.

### UI 프레임워크 변경

기본값은 Gluestack UI v2입니다. 다른 프레임워크를 쓴다면:

1. `templates/component_guide.md`를 해당 프레임워크의 컴포넌트로 교체
2. Phase 2 사전 인터뷰에서 기술 스택 변경을 알려주면 됩니다

### 워크플로우 변경

`CLAUDE.md`를 수정하면 Claude Code의 전체 동작 방식을 바꿀 수 있습니다.

## 프로젝트 구조

```
screen-def-generator/
├── CLAUDE.md                  # Claude Code 지시 파일 (핵심)
├── README.md                  # 이 파일
├── LICENSE                    # MIT 라이선스
├── templates/
│   ├── screen_template.md     # 화면정의서 빈 템플릿
│   ├── screen_example.md      # 완성 예시
│   └── component_guide.md     # UI 컴포넌트 가이드
├── input/                     # PRD 파일을 넣는 폴더
├── output/                    # 생성된 화면정의서 저장 폴더
└── scripts/
    ├── convert_docx.sh        # docx → txt 변환 스크립트
    └── convert_to_html.py     # MD → HTML 변환 스크립트
```

## 요구 사항

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 설치 필요
- macOS (docx 변환 시 `textutil` 사용)
- Python 3 (HTML 변환 시 사용, 외부 패키지 불필요)
