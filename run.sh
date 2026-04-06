#!/bin/zsh
# PPT 파이프라인 실행 스크립트
# 사용법:
#   ./run.sh               → slides/*.html 전체 변환
#   ./run.sh slides/foo.html  → 특정 파일만 변환

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# venv 활성화
source "$SCRIPT_DIR/venv/bin/activate"

# playwright 브라우저 설치 여부 확인
if ! python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.stop()" 2>/dev/null; then
  echo "[설치] Playwright 브라우저 설치 중..."
  playwright install chromium
fi

# 변환 실행
if [ -n "$1" ]; then
  python3 convert.py "$1"
else
  python3 convert.py
fi

echo ""
echo "[결과] output/ 폴더 확인:"
ls -lh output/*.pdf 2>/dev/null || echo "  PDF 없음"
