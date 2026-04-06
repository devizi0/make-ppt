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

- 슬라이드당 핵심 메시지 1개
- 텍스트 최대 5줄, 초과 금지
- 강조색은 `#3182f6` (토스 블루) 단 1개
- 카드 `border-radius: 24px`, 배경 `#f8f9fa` (라이트) / `#141414` (다크)
- **구분선(divider) 절대 금지** — 제목 아래 파란 줄(`width:64px; height:4px`) 사용 금지
- 타이틀 순서: 타이틀 → 목차 → 본문 × N → 마무리

#### 슬라이드 유형별 레이아웃

| 유형 | 레이아웃 |
|------|----------|
| 타이틀 | 좌측 정렬, 태그→헤드라인→서브, 배경 `#0a0a0a` |
| 목차 | 제목 + 2열 카드 그리드 (divider 없음) |
| 본문(리스트) | 좌측 상단 제목만 (섹션 레이블·부제목 금지) + 아이템 리스트 (tossface 아이콘) |
| 본문(카드) | 좌측 상단 제목만 (섹션 레이블·부제목 금지) + 3열 카드 그리드 (각 카드에 tossface 이모지) |
| 비교 | 좌측 상단 제목만 (섹션 레이블·부제목 금지) + 2컬럼 분할, 각 컬럼에 카드 |
| 마무리 | 중앙 정렬, tossface 큰 이모지 + 헤드라인 + CTA |

#### 본문 슬라이드 금지 항목 (AI스러운 느낌 제거)

- **섹션 레이블 절대 금지**: `01 / 스택(Stack)` 같은 `.label` 요소 사용 금지
- **제목 아래 부제목 금지**: 제목(h2) 바로 아래 설명 한 줄 추가 금지
- **본문 슬라이드 레이아웃**: 좌측 상단에 제목(h2)만, 그 아래 콘텐츠 — divider(파란 줄) 절대 금지

#### 비교 슬라이드 레이아웃 규칙

2개 항목을 비교할 때:

- 좌우 2컬럼을 **세로 중간선 하나**로만 구분 (`border-right: 2px solid #e4e4e7` 또는 `<div>` 구분선)
- 각 컬럼에 **박스·테두리·배경색 금지** — 배경은 슬라이드 전체 흰색 그대로
- 컬럼 내부 행 구분은 얇은 가로선(`border-bottom: 1px solid #f0f0f0`)만 허용
- 컬럼 제목은 크고 굵게, 색으로만 좌우를 구분 (테두리·배경 사용 금지)

#### 카드 디자인 규칙 (소형 불릿 카드)

활용 사례, 특징 나열 등 작은 항목을 카드로 나열할 때:

- 배경: `#f4f4f5` (단순 연회색), 화려한 컬러 배경 금지
- 테두리: `border: 1.5px solid #e4e4e7` (얇고 단순한 선)
- `border-radius: 16px` (살짝만 둥글게)
- 패딩: `20px 24px` (작고 컴팩트하게)
- 이모지/아이콘은 작게 (28~32px), 텍스트 앞 인라인 배치
- 카드 제목: `font-size: 20px`, 설명: `font-size: 17px; color: #71717a`
- 태그(Stack/Queue 구분 등)는 제거하거나 아주 작은 dot(●)으로 대체

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
- **에셋 사용 허용 슬라이드**: 타이틀(첫 장), 마무리(끝 장), 섹션 안내(중간 구분) 슬라이드에만 사용
- **에셋 사용 금지 슬라이드**: 목차, 본문(리스트/카드/비교) 슬라이드 — 콘텐츠 가독성 우선
- 다크 슬라이드에는 배경 에셋 또는 오른쪽배치 에셋 중 1개만 선택 사용 (중복 금지)
- 흰 배경 슬라이드에는 `deco-right-purple.png`(보라)만 허용, 나머지 에셋 금지
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
