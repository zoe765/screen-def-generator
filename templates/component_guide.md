# Gluestack UI v2 컴포넌트 가이드

> 화면정의서 생성 시 반드시 이 가이드의 규칙을 준수할 것

---

## 1. 스타일링 시스템 개요

Gluestack UI v2는 NativeWind + Tailwind CSS 기반의 유니버설 컴포넌트 라이브러리입니다.
React + React Native 모두 지원하며, className 기반 스타일링을 사용합니다.

| 축      | 설명                       | 예시                                   |
| ------- | -------------------------- | -------------------------------------- |
| variant | 컴포넌트의 시각적 변형     | solid, outline, link                   |
| action  | 컴포넌트의 의미/색상 계열  | primary, secondary, positive, negative |
| size    | 컴포넌트의 크기            | xs, sm, md, lg, xl                     |

---

## 2. 정보 위계별 컴포넌트 매핑

### Primary Information (핵심 정보) — 스크롤 없이 즉시 인지

| 정보 성격        | 권장 컴포넌트           | 이유                     |
| ---------------- | ----------------------- | ------------------------ |
| 단일 숫자/지표   | Card + stat 텍스트      | 시선 집중, 구조적 경계   |
| 현재 상태        | Badge (action 지정)     | 색상으로 즉시 인지       |
| 단일 텍스트 요약 | Card > Heading + Text   | 제목-설명 위계 유지      |
| AI 생성 결과물   | Card + ScrollView       | 길이 불확정 대응         |
| 진행률           | Progress + Card 래핑    | 수치와 시각 동시 전달    |

> **선택 금지**: Primary Information에 Accordion, Tabs 사용 금지. 클릭 없이 보여야 한다.

### Secondary Information (보조 정보) — 인터랙션 허용

| 정보 성격        | 권장 컴포넌트          | 이유                   |
| ---------------- | ---------------------- | ---------------------- |
| 카테고리별 분류  | Tabs                   | 공간 효율, 맥락 전환   |
| 접기/펼치기 상세 | Accordion              | 선택적 탐색            |
| 관계된 항목들    | Card 그리드 (2~3열)    | 병렬 비교              |
| 메타 정보        | Badge + inline Text    | 시각적 노이즈 최소화   |
| 도움말/힌트      | Tooltip                | 공간 비점유            |

---

## 3. Primary Action 의사결정 트리

```
되돌릴 수 있는가?
  YES → Button (action="primary" 또는 "secondary")
  NO  → AlertDialog + Button (trigger)

결과를 기다려야 하는가?
  YES (즉시) → Button with Spinner
  YES (긴 작업) → Button → Modal/Actionsheet (진행 상황)

입력이 필요한가?
  단순 1개 → Popover + Input + Button
  복잡한 입력 → Modal + FormControl
  다단계 → Actionsheet (사이드 패널, 스텝 포함)
```

---

## 4. Edge Cases & Error Handling 매핑

```
오류 범위:
  전체 화면 차단 → Card + Icon + Text + Button (EmptyState 패턴)
  부분 영역 오류 → Alert (action="error")
  일시적 알림 → Toast
  폼 유효성 → FormControl.ErrorMessage
  데이터 없음 → Card (EmptyState 패턴)

긴급도:
  즉시 해결 → Alert action="error"
  참고 경고 → Alert action="warning"
  안내 → Alert action="info"
  성공 피드백 → Toast action="success" (auto-dismiss 3~5초)
```

---

## 5. 의도 기반 표기법 사전

화면정의서에서 `[ ]` 안에 의도를 적으면 아래 Gluestack UI v2 컴포넌트로 변환됩니다.

### 정보 표시

| 의도 표기                    | Gluestack UI v2 컴포넌트         |
| ---------------------------- | -------------------------------- |
| [카드형 요약]                | Card                             |
| [숫자 강조 표시]             | Card + Heading (size="xl")       |
| [현재 상태 표시]             | Badge                            |
| [펼칠 수 있는 목록]          | Accordion                        |
| [탭으로 나뉜 내용]           | Tabs                             |
| [스크롤 가능한 긴 내용]      | ScrollView                       |
| [진행 상태 바]               | Progress                         |
| [마우스 올리면 나오는 설명]  | Tooltip                          |
| [클릭하면 나오는 작은 패널]  | Popover                          |
| [사용자 프로필 이미지]       | Avatar                           |

### 액션

| 의도 표기                  | Gluestack UI v2 컴포넌트                          |
| -------------------------- | ------------------------------------------------- |
| [메인 버튼]                | Button action="primary" variant="solid"            |
| [보조 버튼]                | Button action="secondary" variant="outline"        |
| [위험한 버튼]              | Button action="negative" variant="solid"           |
| [텍스트 링크형 버튼]       | Button variant="link" / Link                       |
| [아이콘만 있는 버튼]       | Button variant="solid" size="sm" (Icon만 포함)     |
| [확인 팝업 후 실행]        | AlertDialog + Button                               |
| [더보기 메뉴]              | Menu                                               |
| [하단 슬라이드 패널]       | Actionsheet                                        |
| [화면 중앙 팝업]           | Modal                                              |
| [플로팅 액션 버튼]         | Fab                                                |

### 입력

| 의도 표기                | Gluestack UI v2 컴포넌트 |
| ------------------------ | ------------------------ |
| [텍스트 입력]            | Input                    |
| [여러 줄 텍스트 입력]    | Textarea                 |
| [드롭다운 선택]          | Select                   |
| [단일 선택 (2~5개)]      | Radio                    |
| [다중 선택]              | Checkbox                 |
| [켜기/끄기 토글]         | Switch                   |
| [범위 조절]              | Slider                   |

### 피드백

| 의도 표기              | Gluestack UI v2 컴포넌트                             |
| ---------------------- | ---------------------------------------------------- |
| [잠깐 뜨는 알림]       | Toast                                                |
| [고정 오류 메시지]     | Alert action="error"                                 |
| [고정 경고 메시지]     | Alert action="warning"                               |
| [고정 안내 메시지]     | Alert action="info"                                  |
| [고정 성공 메시지]     | Alert action="success"                               |
| [데이터 없음 화면]     | Card (EmptyState 직접 구성)                          |
| [폼 입력 오류]         | FormControl + FormControlError + FormControlErrorText |
| [로딩 중]              | Spinner                                              |
| [이미지]               | Image                                                |

---

## 6. 10가지 컴포넌트 금지 규칙

| #  | 규칙                                                                              | 대안                                     |
| -- | --------------------------------------------------------------------------------- | ---------------------------------------- |
| 1  | Modal 중첩 금지 — Modal 안에 또 다른 Modal 트리거하지 않기                       | Actionsheet → Modal 단방향 계층          |
| 2  | Toast는 영구 정보에 사용 금지 — 사라지면 안 되는 정보(오류, 상태)는 Alert 사용   | Alert                                    |
| 3  | Accordion은 Primary Information에 사용 금지 — 접혀 있으면 안 보임                | 항상 펼침                                |
| 4  | FlatList 행당 액션 버튼 3개 이상 금지                                            | Menu로 묶기                              |
| 5  | Spinner 대신 Skeleton은 레이아웃 예측 가능할 때만 — 형태 미정이면 Spinner 사용   | Spinner                                  |
| 6  | Badge 5개 이상 나열 금지 — 가독성 급락                                           | ScrollView/필터 패턴으로 전환            |
| 7  | Select는 6개 미만 옵션에 사용 금지 — 2~5개는 Radio가 더 명확                     | Radio                                    |
| 8  | Tooltip은 모바일 퍼스트에 사용 금지 — 터치에 hover 없음                          | Popover로 대체                           |
| 9  | FormControl 없이 Input 단독 사용 금지 (유효성 검사 필요 시)                      | FormControl + Input 패턴 필수            |
| 10 | AlertDialog는 되돌림 가능 액션에 사용 금지                                       | 삭제/발행/초기화 등 비가역 액션 전용     |

---

## 7. 감정 키워드 × Gluestack UI v2 스타일 매핑표

| Emotional Direction | Card className                      | Badge action | Button (Primary)                        | Alert action | Toast action | 간격     |
| ------------------- | ----------------------------------- | ------------ | --------------------------------------- | ------------ | ------------ | -------- |
| 신뢰                | border-outline-200 shadow-soft-1    | info         | action="primary" className="px-8"       | info         | success      | gap-6~8  |
| 성취감              | border-primary-200 shadow-soft-2    | success      | action="positive" size="lg"             | success      | success      | gap-6    |
| 긴장/경고           | border-error-300                    | error        | action="negative"                       | error        | error        | gap-2~3  |
| 효율                | border-outline-200                  | muted        | action="primary"                        | info         | info         | gap-4    |
| 친근함              | shadow-soft-3 rounded-xl            | info         | action="secondary" variant="outline"    | info         | info         | gap-6    |
| 전문성              | border-outline-300 shadow-none      | muted        | action="primary"                        | info         | info         | gap-4~5  |
