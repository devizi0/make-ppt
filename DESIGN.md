# PPT 디자인 가이드

토스(Toss) 스타일 기반 슬라이드 디자인 시스템.

---

## 핵심 원칙

1. **여백이 곧 디자인** — 콘텐츠보다 여백이 많아야 한다
2. **텍스트 위계** — 크기 차이로 정보 계층을 만든다
3. **색은 최소** — 배경 + 텍스트 + 강조색 1개 (필요시 빨강·초록 등 추가 허용)
4. **이모지는 토스페이스** — 시스템 이모지 절대 사용 금지
5. **콘텐츠를 충분히 담되, 레이아웃은 미니멀하게**

---

## 색상 시스템

### 강조색
```css
--accent: #3852B4;          /* 기본 강조색 */
--accent-light: #5b75d4;    /* 연한 변형 */
--accent-lighter: #7b93e0;  /* 더 연한 변형 */
```

필요에 따라 빨강(`#e53e3e`), 초록(`#38a169`), 주황 등 의미 전달에 필요한 색상은 유연하게 사용 가능.

### 다크 테마 (타이틀/강조 슬라이드 전용)
```css
--bg-dark:        #0a0a0a;
--text-primary:   #ffffff;
--text-secondary: rgba(255,255,255,0.7);
--text-muted:     rgba(255,255,255,0.3~0.5);
--border:         rgba(255,255,255,0.08);
```

**다크 배경 색상 규칙:**
- 본문 텍스트: `#ffffff` 또는 `rgba(255,255,255,0.7~0.9)` — 검정/어두운 색 절대 금지
- 강조 텍스트: `#3852B4` 대신 밝은 계열(`#7b93e0`, `#a0b4f0`) 우선 사용
- `#09090b`, `#3f3f46`, `#71717a` 등 어두운 색 다크 배경에 절대 사용 금지

### 라이트 테마 (본문 슬라이드 기본)
```css
--bg-light:       #ffffff;
--text-primary:   #09090b;
--text-secondary: #71717a;
--text-muted:     #a1a1aa;
--border:         #e4e4e7;
```

### 배경 규칙 (엄수)
| 슬라이드 유형 | 허용 배경 |
|---|---|
| 타이틀 (첫 장) | `#0a0a0a` 단색 다크 |
| 마무리 (끝 장) | `#0a0a0a` 단색 다크 |
| 목차 / 본문 | `#ffffff` 완전 흰색 |
| 강조 섹션 | `#0a0a0a` 완전 검정 |
| **그라디언트** | **타이틀/마무리에만 허용, 본문 절대 금지** |
| **회색 배경** | **절대 금지 — 흰색 또는 검정만** |

---

## 타이포그래피

### 기본 폰트 (사용자 지시 없으면 Freesentation 사용)
```css
/* 기본 */
font-family: 'Freesentation', sans-serif;

/* 대안 */
font-family: 'Wanted Sans Variable', sans-serif;
```

하나의 HTML 파일에 폰트 1종만 사용. 혼합 금지.
토스페이스(이모지)는 항상 `font-family` 맨 앞에 배치.

### 텍스트 스케일 (1920×1080 기준)
| 용도 | 크기 | 굵기 |
|---|---|---|
| 메인 헤드라인 | 120~150px | 800 |
| 섹션 제목 | 62~82px | 800 |
| 서브 제목 | 32~44px | 600 |
| 본문 | 22~28px | 300~400 |
| 캡션/레이블 | 18~20px | 500~600 |
| 칩/태그 | 22~26px | 500 |
| 숫자 강조 | 92~120px | 800 |

**얇은 폰트(100~300) 적극 활용** — 부제목·설명·서브텍스트에 사용. 굵기 대비가 클수록 세련됨.

### 자간
```css
/* 헤드라인 */
letter-spacing: -0.03em ~ -0.05em;

/* 본문 */
letter-spacing: -0.01em ~ -0.02em;

/* 레이블 (대문자) */
letter-spacing: 0.06em ~ 0.08em;
```

---

## 이모지 — 토스페이스

반드시 로컬 파일 사용 — CDN 방식은 Playwright PDF 변환 시 동작 안 함.

```css
@import url('../fonts/tossface.css');
.tossface { font-family: "Tossface", "Freesentation", sans-serif; font-style: normal; }
```

```html
<span class="tossface" style="font-size:48px">🚀</span>
```

---

## 레이아웃 시스템

### 슬라이드 기본 구조
```css
.slide {
  width: 1920px;
  height: 1080px;
  position: relative;
  overflow: hidden;
  page-break-after: always;
  break-after: page;
}

/* 타이틀/마무리 */
.slide-title {
  display: flex; flex-direction: column; justify-content: center;
  padding: 0 180px;
}

/* 본문 슬라이드 */
.slide-content {
  display: flex; flex-direction: column; justify-content: space-between;
  padding: 90px 90px 80px;
}
```

### 배경 이미지 패턴
```html
<div class="slide slide-content">
  <img style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.25;" src="../assets/bg-light-1.png">
  <div style="position:relative;z-index:1;display:flex;flex-direction:column;flex:1;justify-content:space-between;">
    <!-- 상단: 로고 + 제목 -->
    <!-- 하단: 콘텐츠 그리드 -->
  </div>
</div>
```

**주의**: 내부 wrapper에 `height:100%` 금지 — 슬라이드 padding을 무시하고 콘텐츠가 넘침. `flex:1` 사용.

### border 구분선 그리드 (카드 대신 선으로 구분)
```css
/* 4열 (흰 배경) */
.cols-4 { display: grid; grid-template-columns: repeat(4,1fr); border-top: 1px solid #e4e4e7; }
.col { padding: 56px 46px 0 0; border-right: 1px solid #e4e4e7; }
.col:last-child { border-right: none; padding-right: 0; }
.col + .col { padding-left: 46px; }

/* 4열 (다크 배경) */
.cols-4-dark { display: grid; grid-template-columns: repeat(4,1fr); border-top: 1px solid rgba(255,255,255,0.08); }
.col-dark { padding: 56px 46px 0 0; border-right: 1px solid rgba(255,255,255,0.08); }
.col-dark:last-child { border-right: none; padding-right: 0; }
.col-dark + .col-dark { padding-left: 46px; }

/* 3열도 동일 패턴 (cols-3 / cols-3-dark) */
```

---

## 에셋 시스템

에셋은 `assets/` 디렉토리. HTML에서 `../assets/파일명`으로 참조.

### 다크 배경 에셋
| 파일 | 색상 | 적합한 슬라이드 |
|------|------|----------------|
| `bg-dark-1-blur.png` | 검정+핑크/틸 물결 | 타이틀, 마무리 |
| `bg-dark-2-blur.png` | 검정+레드/오렌지 글로우 | 강조 섹션 |
| `bg-dark-3.png` | 검정+레드/틸 유기적 곡선 | 타이틀 |
| `bg-dark-4-blur.png` | 검정+핑크/퍼플 보케 | 마무리 |
| `bg-dark-5.png` | 검정+레드/퍼플 입체 곡선 | 섹션 구분 |
| `bg-dark-6.png` | 검정+딥 네이비 웨이브 | 강조 본문 |
| `bg-dark-7-blur.png` | 검정+딥 네이비 소프트 블러 | 타이틀, 마무리 |

### 흰색 배경 에셋
| 파일 | 색상 |
|------|------|
| `bg-light-0.png` | 하늘색+퍼플 홀로그램 물결 |
| `bg-light-1.png` | 하늘색+라벤더 소프트 그라디언트 |

opacity: 0.22~0.30 권장.

### 오른쪽 장식 에셋 (deco-right)
| 파일 | 색상 |
|------|------|
| `deco-right-blue.png` | 파랑 반원+글로우 |
| `deco-right-orange.png` | 주황/레드 반원+글로우 |
| `deco-right-purple.png` | 보라/바이올렛 반원+글로우 |

**사용 전 반드시 3가지 조건 전부 확인할 것:**
1. 흰색 배경 슬라이드인가?
2. **모든** 콘텐츠가 슬라이드 좌측에만 배치되는가? (그리드·양쪽 콘텐츠 있으면 불가)
3. 슬라이드 우측이 **완전히** 비어있는가?

→ 3가지 모두 YES일 때만 사용. 하나라도 NO면 즉시 `bg-light-0/1`로 대체.
→ 슬라이드 콘텐츠를 먼저 배치한 뒤, 우측이 비어있는지 확인 후 추가할 것 — 먼저 넣고 보는 방식 금지.
→ deco-right와 bg-* 동시 사용 금지.

```html
<img style="position:absolute;right:0;top:0;bottom:0;height:100%;width:auto;object-fit:cover;object-position:left center;z-index:1;" src="../assets/deco-right-blue.png">
```

---

## 금지 사항

- **상하 구분선 금지** — 제목 아래 파란 줄(`width:64px; height:4px`) 등 수평 장식선 절대 금지
- **좌우 구분선(세로선)은 허용** — 컬럼 사이 `border-right` 패턴은 적극 사용
- **제목에 구분 기호 금지** — 제목에 `-`, `—`, `ㅡ` 삽입 금지
- **중앙 정렬 남발 금지** — 마무리 슬라이드 외엔 좌측 정렬
- **카드 박스 남발 금지** — 선(border) 하나로 대체 우선
- **섹션 레이블 남발 금지** — `01 / 제목` 형태 사용 금지
- **과한 색상 금지** — 컬러 배경 카드, 그라디언트 텍스트 금지
- 본문 슬라이드에 그라디언트 배경 사용
- 시스템 기본 이모지 사용 (토스페이스로 대체)
- 배경이 회색 계열 (#ffffff, #0a0a0a만 허용)
- CSS로 만든 단순 원형 장식 — 반드시 에셋 파일 사용

---

## 슬라이드 유형별 레이아웃

| 유형 | 레이아웃 |
|------|----------|
| 타이틀 | 좌측 정렬, eyebrow → 이름/제목(초대형) → role → 설명, 배경 `#0a0a0a` |
| 숫자 강조 | 4열 border 그리드 — 숫자 초대형(120px+), 레이블 작게 |
| 본문(리스트형) | 제목 + 카테고리 레이블(회색) + 칩(chip) 나열 |
| 본문(지표형) | 제목 + metric(숫자 초대형 + 설명 작게), border로만 구분 |
| 본문(포인트형) | 제목 + 설명 + 4열 포인트(아이콘+제목+설명), border로만 구분 |
| 본문(테이블형) | 제목 + 행 목록, 각 행은 border-bottom으로 구분 |
| 마무리 | 좌측 정렬, eyebrow → 헤드라인(초대형, "감사합니다"로 끝) → 연락처, 배경 `#0a0a0a` |
