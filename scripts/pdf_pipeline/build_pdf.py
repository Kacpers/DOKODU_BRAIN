#!/usr/bin/env python3
"""
DOKODU PDF Pipeline — HTML/CSS → PDF
Usage:
    python build_pdf.py chapters/01_automatyzacja_polska.html        # single chapter
    python build_pdf.py chapters/*.html -o build/ebook_full.pdf      # merge all
    python build_pdf.py chapters/01.html --engine playwright         # use playwright
    python build_pdf.py chapters/01.html --engine weasyprint         # use weasyprint
"""

import argparse
import sys
from pathlib import Path


def build_with_playwright(html_paths: list[Path], output: Path):
    """Pixel-perfect rendering, jak przeglądarka. Lepszy do ofert."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        if len(html_paths) == 1:
            file_url = html_paths[0].resolve().as_uri()
            page.goto(file_url, wait_until="networkidle")
            page.pdf(
                path=str(output),
                format="A4",
                margin={"top": "25mm", "right": "20mm", "bottom": "30mm", "left": "20mm"},
                print_background=True,
            )
            print(f"  [playwright] {output} ({output.stat().st_size // 1024} KB)")
        else:
            # Merge: concatenate HTML bodies
            combined = _merge_html(html_paths)
            tmp = output.parent / "_combined_tmp.html"
            tmp.write_text(combined, encoding="utf-8")
            page.goto(tmp.resolve().as_uri(), wait_until="networkidle")
            page.pdf(
                path=str(output),
                format="A4",
                margin={"top": "25mm", "right": "20mm", "bottom": "30mm", "left": "20mm"},
                print_background=True,
            )
            tmp.unlink()
            print(f"  [playwright] {output} ({output.stat().st_size // 1024} KB)")

        browser.close()


def build_with_weasyprint(html_paths: list[Path], output: Path):
    """Print-layout oriented. Lepszy do ebooków z @page rules."""
    import weasyprint

    if len(html_paths) == 1:
        doc = weasyprint.HTML(filename=str(html_paths[0]))
        doc.write_pdf(str(output))
        print(f"  [weasyprint] {output} ({output.stat().st_size // 1024} KB)")
    else:
        combined = _merge_html(html_paths)
        tmp = output.parent / "_combined_tmp.html"
        tmp.write_text(combined, encoding="utf-8")
        doc = weasyprint.HTML(filename=str(tmp), base_url=str(html_paths[0].parent))
        doc.write_pdf(str(output))
        tmp.unlink()
        print(f"  [weasyprint] {output} ({output.stat().st_size // 1024} KB)")


def _merge_html(html_paths: list[Path]) -> str:
    """Merge multiple HTML files into one, keeping first <head>."""
    from bs4 import BeautifulSoup

    first = BeautifulSoup(html_paths[0].read_text(encoding="utf-8"), "html.parser")
    for path in html_paths[1:]:
        doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        body = doc.find("body")
        if body:
            for child in body.children:
                first.body.append(child.__copy__() if hasattr(child, '__copy__') else child)
    return str(first)


def main():
    parser = argparse.ArgumentParser(description="DOKODU PDF Pipeline")
    parser.add_argument("inputs", nargs="+", type=Path, help="HTML files to convert")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output PDF path")
    parser.add_argument("--engine", choices=["playwright", "weasyprint"], default="playwright",
                        help="Rendering engine (default: playwright)")
    args = parser.parse_args()

    # Resolve inputs
    html_files = []
    for p in args.inputs:
        if p.is_file():
            html_files.append(p)
        else:
            print(f"Warning: {p} not found, skipping")

    if not html_files:
        print("No HTML files found.")
        sys.exit(1)

    # Output path
    if args.output:
        output = args.output
    else:
        output = Path("build") / html_files[0].with_suffix(".pdf").name

    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Building PDF: {len(html_files)} file(s) → {output}")
    print(f"Engine: {args.engine}")

    if args.engine == "playwright":
        build_with_playwright(html_files, output)
    else:
        build_with_weasyprint(html_files, output)

    print("Done!")


if __name__ == "__main__":
    main()
