#!/usr/bin/env python3
"""
HTML → PDF 변환기
Playwright headless 브라우저로 슬라이드를 PDF로 변환
"""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080


async def html_to_pdf(html_path: Path, output_path: Path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": SLIDE_WIDTH, "height": SLIDE_HEIGHT}
        )

        await page.goto(f"file://{html_path.resolve()}")
        await page.wait_for_load_state("networkidle")

        await page.pdf(
            path=str(output_path),
            width=f"{SLIDE_WIDTH}px",
            height=f"{SLIDE_HEIGHT}px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        await browser.close()
    print(f"[완료] {output_path.name} 저장됨")


async def main():
    slides_dir = Path(__file__).parent / "slides"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # 변환 대상 파일 결정
    if len(sys.argv) > 1:
        targets = [Path(sys.argv[1])]
    else:
        targets = sorted(slides_dir.glob("*.html"))

    if not targets:
        print("[오류] slides/ 폴더에 HTML 파일이 없습니다.")
        sys.exit(1)

    for html_file in targets:
        if not html_file.exists():
            print(f"[오류] 파일 없음: {html_file}")
            continue
        pdf_path = output_dir / (html_file.stem + ".pdf")
        print(f"[변환] {html_file.name} → {pdf_path.name}")
        await html_to_pdf(html_file, pdf_path)


if __name__ == "__main__":
    asyncio.run(main())
