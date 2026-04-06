# PPT 파이프라인

이 디렉토리는 HTML 슬라이드를 작성하고 PDF로 변환하는 파이프라인이다.
디자인 상세 규칙은 `DESIGN.md` 참고.

---

## /ppt 슬라이드 생성

사용자가 `/ppt <주제>` 또는 슬라이드 제작을 요청하면 아래 절차를 따른다.

### 1. HTML 파일 생성

`slides/<파일명>.html` 에 슬라이드를 작성한다.

#### 필수 규칙

- **해상도**: 1920×1080px (16:9), `body { width: 1920px; }`
- **슬라이드 단위**: `<div class="slide">` 하나 = PDF 1페이지
- `page-break-after: always` + `break-after: page` 반드시 포함
- `print_background: true` 대응 — 배경색 CSS에 반드시 명시
- 폰트: `'Pretendard', -apple-system, 'Apple SD Gothic Neo', sans-serif`
- **이모지: 반드시 토스페이스 사용** (로컬 `fonts/` 디렉토리의 woff2 파일 + `.tossface` 클래스)
- 외부 리소스는 `<link>` 태그로 `<head>`에 삽입
- **토스페이스는 반드시 로컬 파일 사용** — CDN `<link>` 금지 (Playwright file:// 프로토콜에서 상대경로 미동작)

#### 배경색 규칙 (엄수)

| 슬라이드 유형 | 배경 |
|---|---|
| 타이틀 (첫 장) | `#0a0a0a` |
| 마무리 (끝 장) | `#0a0a0a` |
| 목차 / 본문 | `#ffffff` |
| 강조 섹션 | `#0a0a0a` |
| **그라디언트** | **타이틀·마무리에만 허용, 본문 절대 금지** |
| **회색 배경** | **절대 금지 — 흰색 또는 검정만** |

#### 토스페이스 이모지 사용법

**반드시 로컬 파일 사용** — CDN `<link>` 방식은 Playwright PDF 변환 시 동작 안 함.

```html
<head>
<style>
  /* 토스페이스 로컬 폰트 — fonts/ 디렉토리 기준 상대경로 */
  @font-face { font-family:"Tossface"; src:url("../fonts/TossFaceFontMac-00.woff2") format("woff2"); unicode-range:U+200D,U+FE0F,...; }
  /* ... 나머지 @font-face 동일 패턴 */
  .tossface { font-family:"Tossface","Apple Color Emoji",sans-serif; font-style:normal; }
</style>
</head>

<!-- 사용 -->
<span class="tossface" style="font-size:56px">🚀</span>
```

실제 슬라이드 작성 시: `fonts/tossface.css` 파일을 `<style>` 태그 안에 `@import`하거나 내용을 인라인으로 붙여넣는다.

#### 사용 가능한 본문 폰트 (슬라이드 1개당 1종만 선택)

| 폰트 | CSS 파일 | `font-family` | 특징 |
|------|----------|---------------|------|
| Freesentation | `fonts/freesentation.css` | `'Freesentation'` | 발표용 한글 폰트, weight 100~900 |
| Wanted Sans | `fonts/wanted-sans.css` | `'Wanted Sans Variable'` | 가변 웹폰트, 현대적 산세리프 |

**규칙**
- **기본 폰트: Freesentation** — 사용자가 별도 지시하지 않으면 항상 Freesentation 사용
- 하나의 PPT HTML 파일에는 반드시 하나의 본문 폰트만 사용
- Freesentation / Wanted Sans 혼합 절대 금지
- 토스페이스(이모지) 폰트는 항상 최우선 적용 — `font-family` 맨 앞에 `"Tossface"` 배치

```css
/* Freesentation 사용 예 */
@import url('../fonts/tossface.css');
@import url('../fonts/freesentation.css');
body { font-family: 'Freesentation', sans-serif; }
.tossface { font-family: "Tossface", "Freesentation", sans-serif; }

/* Wanted Sans 사용 예 */
@import url('../fonts/tossface.css');
@import url('../fonts/wanted-sans.css');
body { font-family: 'Wanted Sans Variable', sans-serif; }
.tossface { font-family: "Tossface", "Wanted Sans Variable", sans-serif; }
```

#### 기본 HTML 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>제목</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/toss/tossface/dist/tossface.css">
<style>
  @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1920px; font-family: 'Pretendard', -apple-system, 'Apple SD Gothic Neo', sans-serif; }

  .slide {
    width: 1920px;
    height: 1080px;
    position: relative;
    overflow: hidden;
    page-break-after: always;
    break-after: page;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 120px 140px;
  }
</style>
</head>
<body>
  <div class="slide slide-title"> ... </div>
  <div class="slide slide-toc"> ... </div>
  <div class="slide slide-content"> ... </div>
  <div class="slide slide-end"> ... </div>
</body>
</html>
```

#### 토스 스타일 디자인 원칙

**핵심 철학: 극도로 미니멀 — 여백이 디자인이다**

- 슬라이드당 핵심 메시지 1개, 텍스트 최대 5줄
- **제목에 구분 기호 금지**: 제목(h1/h2/슬라이드 타이틀)에 `-`, `—`, `ㅡ` 등 구분선 기호 삽입 금지 — 제목은 순수 텍스트만
- **강조색**: 기본 `#3852B4`, 더 연한 변형(`#5b75d4`, `#7b93e0` 등) 허용. 필요에 따라 빨강(`#e53e3e`), 초록(`#38a169`), 주황 등 의미 전달에 필요한 색상은 유연하게 사용 가능
- **다크 배경(검정) 슬라이드 색상 규칙**:
  - 본문 텍스트: `#ffffff` 또는 `rgba(255,255,255,0.7~0.9)` — 검정/어두운 색 절대 금지
  - 강조 텍스트: `#3852B4` 대신 밝은 계열(`#7b93e0`, `#a0b4f0`) 우선 사용
  - 서브 텍스트: `rgba(255,255,255,0.3~0.5)`
  - `#09090b`, `#3f3f46`, `#71717a` 등 어두운 색 다크 배경에 절대 사용 금지
- 폰트 위계 명확: 제목 크고 굵게(700~800), 본문 얇게(300~400). **얇은 폰트(100~300)는 부제목·설명·서브텍스트에 적극 활용** — 굵기 대비가 클수록 세련된 느낌
- **숫자/지표는 크게** — `font-size: 64px~120px`, 나머지는 작게
- 여백을 아끼지 말 것 — `padding: 0 160px`, 요소 간 `gap` 충분히
- **카드 남발 금지** — 카드 없이 선(`border`) 하나로 구분하는 것을 우선 고려
- **상하 구분선 금지** — 제목 아래 파란 줄(`width:64px; height:4px`) 등 수평 장식선 절대 금지. 콘텐츠 사이 불필요한 `border-top/bottom`도 금지
- **좌우 구분선(세로선)은 허용** — 컬럼 사이 `border-right: 1px solid #e4e4e7` 패턴은 적극 사용
- `-webkit-font-smoothing: antialiased` 항상 적용
- `letter-spacing: -0.02em ~ -0.04em` — 큰 텍스트는 자간 좁게
- 타이틀 순서: 타이틀 → 본문 × N → 마무리

#### 슬라이드 유형별 레이아웃

| 유형 | 레이아웃 |
|------|----------|
| 타이틀 | 좌측 정렬, eyebrow(작은 설명) → 이름/제목(초대형) → role → 설명, 배경 `#0a0a0a` |
| 숫자 강조 | 좌우 분할(border로만 구분) — 왼쪽 설명, 오른쪽 2×2 stat 그리드(숫자 초대형) |
| 본문(리스트형) | 제목 + 카테고리 레이블(회색) + 칩(chip) 나열 — 행 단위로 구성 |
| 본문(지표형) | 제목 + 기간 + 가로로 나열한 metric(숫자 초대형 + 설명 작게), border로만 구분 |
| 본문(포인트형) | 제목 + 설명(작게) + 4열 포인트(아이콘+제목+설명), border로만 구분 |
| 본문(테이블형) | 제목 + 행 목록, 각 행은 border-bottom으로 구분 — 날짜/아이콘/제목/출처 |
| 마무리 | 좌측 정렬, eyebrow → 헤드라인(초대형) → 연락처(작게), 배경 `#0a0a0a`. **헤드라인은 반드시 "감사합니다" 또는 이와 유사한 감사 인사로 끝낼 것** |

#### 금지 항목 (AI스러운 느낌 제거)

- **카드 박스 남발 금지**: 배경+테두리가 있는 카드는 꼭 필요한 경우만 — 선 하나(border)로 대체 우선
- **섹션 레이블 남발 금지**: `01 / 제목` 형태 사용 금지
- **제목 아래 부제목 금지**: h2 바로 아래 설명 한 줄 추가 금지
- **divider(파란 줄) 금지**: 제목 아래 장식선 절대 금지
- **과한 색상 금지**: 컬러 배경 카드, 그라디언트 텍스트 금지
- **중앙 정렬 남발 금지**: 마무리 슬라이드 외엔 좌측 정렬 원칙

#### 레이아웃 패턴 (코드 참고)

**슬라이드 수직 레이아웃 핵심 규칙:**
- 타이틀/마무리 슬라이드: `display:flex; flex-direction:column; justify-content:center; padding:0 180px;`
- 본문 슬라이드: **`display:flex; flex-direction:column; justify-content:space-between; padding:90px 90px 80px;`** — 콘텐츠가 슬라이드 전체 높이를 채우도록 상하 여백 확보
- 본문 슬라이드 내부 구조: 배경 `<img>`는 `position:absolute;inset:0`, 콘텐츠는 `position:relative;z-index:1;display:flex;flex-direction:column;height:100%;justify-content:space-between;`으로 감싸서 헤더(로고+제목)와 콘텐츠 그리드가 상하로 분리되도록 할 것
- 배경 이미지는 `position:absolute;inset:0` + 콘텐츠는 `position:relative;z-index:1`로 분리
- **콘텐츠 잘림 방지**: 내부 wrapper에 `height:100%` 절대 사용 금지 — 슬라이드 padding을 무시하고 콘텐츠가 넘침. 대신 슬라이드 자체를 `display:flex`로 두고 wrapper는 `flex:1`로 설정할 것. 배경 img는 `position:absolute`이므로 flex item에서 제외됨

```css
/* 본문 슬라이드 기본 구조 — 슬라이드 전체 높이 활용 */
.slide-content {
  padding: 90px 90px 80px;
  display: flex; flex-direction: column; justify-content: space-between;
}
/* 내부 wrapper: position:relative;z-index:1;display:flex;flex-direction:column;height:100%;justify-content:space-between; */
/* 상단: 로고(margin-bottom:48px) + 제목 / 하단: 콘텐츠 그리드 */

/* 4열 border 구분 그리드 (흰 배경) */
.cols-4 { display: grid; grid-template-columns: repeat(4,1fr); border-top: 1px solid #e4e4e7; }
.col { padding: 36px 40px 0 0; border-right: 1px solid #e4e4e7; }
.col:last-child { border-right: none; padding-right: 0; }
.col + .col { padding-left: 40px; }

/* 4열 border 구분 그리드 (다크 배경) */
.cols-4-dark { display: grid; grid-template-columns: repeat(4,1fr); border-top: 1px solid rgba(255,255,255,0.08); }
.col-dark { padding: 36px 40px 0 0; border-right: 1px solid rgba(255,255,255,0.08); }
.col-dark:last-child { border-right: none; padding-right: 0; }
.col-dark + .col-dark { padding-left: 40px; }

/* 3열도 동일 패턴으로 cols-3 / cols-3-dark 사용 */

/* 숫자 강조 */
.stat-num { font-size: 120px; font-weight: 800; letter-spacing: -0.05em; line-height: 1; }

/* 기술 스택 칩 */
.sk-chip { font-size: 26px; font-weight: 500; color: #3f3f46; background: #f4f4f5; border-radius: 10px; padding: 14px 28px; }
.sk-cat { font-size: 18px; font-weight: 600; color: #a1a1aa; letter-spacing: 0.08em; text-transform: uppercase; width: 230px; }
.skill-row { display: flex; align-items: center; padding: 46px 0; border-bottom: 1px solid #f0f0f0; }

/* 테이블형 행 (성취/자격증 등) */
.achv-row { display: flex; align-items: center; padding: 48px 0; border-bottom: 1px solid #e4e4e7; gap: 44px; }
.achv-row:first-child { border-top: 1px solid #e4e4e7; }
.a-date { font-size: 20px; color: #a1a1aa; width: 100px; }
.a-icon { font-size: 38px; }
.a-name { font-size: 34px; font-weight: 600; color: #09090b; }
.a-org { font-size: 22px; color: #a1a1aa; }

/* 로고 */
.logo { font-size: 20px; font-weight: 700; color: #3852B4; margin-bottom: 52px; display: block; }
.logo-dark { color: rgba(255,255,255,0.38); }

/* 본문 제목 */
.s-h1 { font-size: 62px; font-weight: 800; color: #09090b; letter-spacing: -0.03em; margin-bottom: 52px; }
```

**에셋 사용 규칙 (반드시 준수):**

**대부분의 슬라이드는 bg-light/bg-dark를 쓴다. deco-right는 조건 충족 시만 사용한다.**

- **흰 배경 슬라이드 기본**: `bg-light-0.png` 또는 `bg-light-1.png` (opacity: 0.22~0.30)
- **다크 배경 슬라이드 기본**: `bg-dark-*.png` 중 하나 (opacity: 0.22~0.32)
- **`deco-right-blue/orange/purple.png` 사용 전 반드시 3가지 조건 전부 확인할 것**:
  1. 흰색 배경 슬라이드인가?
  2. **모든** 콘텐츠가 슬라이드 좌측에만 배치되는가? (그리드·양쪽 콘텐츠 있으면 불가)
  3. 슬라이드 우측이 **완전히** 비어있는가?
  → 3가지 모두 YES일 때만 사용. 하나라도 NO면 즉시 bg-light-0/1로 대체
  → 슬라이드 콘텐츠를 먼저 배치한 뒤, 우측이 비어있는지 확인 후 추가할 것 — 먼저 넣고 보는 방식 금지
- deco-right와 bg-* 동시 사용 절대 금지 — 둘 중 하나만

#### 비교 슬라이드 레이아웃 규칙

2개 항목을 비교할 때:

- 좌우 2컬럼을 **세로 중간선 하나**로만 구분 (`border-right: 1px solid #e4e4e7`)
- 각 컬럼에 **박스·테두리·배경색 금지** — 배경은 슬라이드 전체 흰색 그대로
- 컬럼 내부 행 구분은 얇은 가로선(`border-bottom: 1px solid #e4e4e7`)만 허용
- 컬럼 제목은 크고 굵게, 색으로만 좌우를 구분 (테두리·배경 사용 금지)

#### 카드 디자인 규칙 (꼭 써야 할 때만)

- 배경: `#f4f4f5`, 화려한 컬러 배경 금지
- 테두리: `border: 1.5px solid #e4e4e7`
- `border-radius: 16px`, 패딩: `20px 24px`
- 이모지/아이콘: 28~36px, 텍스트 위에 단독 배치
- 카드 제목: `font-size: 22~26px font-weight: 700`, 설명: `font-size: 18~20px; color: #71717a`

#### 배경/장식 에셋 사용법

에셋은 `assets/` 디렉토리에 저장되어 있다. HTML에서 `../assets/파일명` 으로 참조한다.

**다크 배경 에셋 (검정 슬라이드용)**

| 파일 | 색상 | 적합한 슬라이드 |
|------|------|----------------|
| `bg-dark-1-blur.png` | 검정+핑크/틸 물결 | 타이틀, 마무리 |
| `bg-dark-2-blur.png` | 검정+레드/오렌지 글로우 | 강조 섹션 |
| `bg-dark-3.png` | 검정+레드/틸 유기적 곡선 | 타이틀 |
| `bg-dark-4-blur.png` | 검정+핑크/퍼플 보케 | 마무리 |
| `bg-dark-5.png` | 검정+레드/퍼플 입체 곡선 | 섹션 구분 |
| `bg-dark-6.png` | 검정+딥 네이비 웨이브 | 강조 본문 |
| `bg-dark-7-blur.png` | 검정+딥 네이비 소프트 블러 | 타이틀, 마무리 |

**흰색 계열 배경 에셋 (전체 슬라이드 사용 가능)**

| 파일 | 색상 | 적합한 슬라이드 |
|------|------|----------------|
| `bg-light-0.png` | 하늘색+퍼플 홀로그램 물결 텍스처 | 모든 슬라이드 배경 사용 가능 |
| `bg-light-1.png` | 하늘색+라벤더 소프트 그라디언트 | 모든 슬라이드 배경 사용 가능 |

**오른쪽 장식 에셋 (슬라이드 우측에 오버레이)**

| 파일 | 색상 | 사용법 |
|------|------|--------|
| `deco-right-blue.png` | 파랑 반원+글로우 | **흰색 배경 전용** — 다크 배경 사용 금지 |
| `deco-right-orange.png` | 주황/레드 반원+글로우 | **흰색 배경 전용** — 다크 배경 사용 금지 |
| `deco-right-purple.png` | 보라/바이올렛 반원+글로우 | **흰색 배경 전용** — 다크 배경 사용 금지 |

```html
<!-- 다크 배경 전체 채우기 -->
<div class="slide" style="position:relative;">
  <img style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;" src="../assets/bg-dark-1-blur.png">
  <div style="position:relative;z-index:1;"><!-- 콘텐츠 --></div>
</div>

<!-- 오른쪽 장식 에셋 — 상하좌우 슬라이드 끝에 붙게, 이미지 잘려도 됨 -->
<img style="position:absolute;right:0;top:0;bottom:0;height:100%;width:auto;object-fit:cover;object-position:left center;z-index:1;" src="../assets/deco-right-blue.png">
```

**규칙**
- CSS로 만든 `deco-circle` 같은 단순 원형 장식 절대 금지 — 반드시 에셋 파일 사용
- **deco-right-blue/orange/purple.png 사용 조건 (3가지 모두 충족해야 함)**:
  1. 흰색 배경 슬라이드
  2. 콘텐츠가 슬라이드 좌측에만 배치됨
  3. 슬라이드 우측이 비어있음
  → 위 조건 하나라도 불충족 시 사용 금지
- **흰 배경 본문 슬라이드 (일반)**: `bg-light-0.png` 또는 `bg-light-1.png` 사용 (opacity: 0.22~0.30)
- **다크 배경 본문 슬라이드**: `bg-dark-*.png` 중 하나 사용 (opacity: 0.22~0.32)
- deco-right와 bg-* 동시 사용 절대 금지
- 에셋 테스트는 `slides/asset-test.html` 참고

---

### 2. PDF 변환

```bash
cd /Users/ivinx/agent/ppt-pipeline
./run.sh slides/<파일명>.html   # 단일 파일
./run.sh                        # 전체 변환
```

결과물: `output/<파일명>.pdf`

---

## 파일 구조

```
ppt-pipeline/
├── slides/       ← HTML 슬라이드 작성 위치
├── output/       ← 변환된 PDF 저장 위치
├── DESIGN.md     ← 디자인 가이드 (상세)
├── convert.py    ← HTML → PDF 변환기 (수정 금지)
├── run.sh        ← 실행 스크립트
└── venv/         ← Python 가상환경 (수정 금지)
```
