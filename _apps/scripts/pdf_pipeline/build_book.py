#!/usr/bin/env python3
"""DOKODU Book Pipeline — Orchestrator.

Usage:
    python build_book.py <book-slug>                    # build PDF
    python build_book.py <book-slug> --html-only        # HTML only (no PDF)
    python build_book.py <book-slug> --preview          # open after build
"""
import argparse
import sys
from pathlib import Path

# Ensure sibling modules are importable regardless of CWD
sys.path.insert(0, str(Path(__file__).parent))

# Resolve paths
SCRIPT_DIR = Path(__file__).parent
BOOKS_DIR = SCRIPT_DIR.parent.parent.parent / '30_RESOURCES' / 'RES_Ebook' / 'books'
BUILD_DIR = SCRIPT_DIR / 'build'
CSS_PATH = str((SCRIPT_DIR / 'templates' / 'base.css').resolve())


def build_book(book_dir: Path, output_dir: Path | None = None,
               pdf: bool = True) -> Path:
    """Build a book from Markdown to HTML (and optionally PDF).

    Returns path to the generated file (HTML or PDF).
    """
    from md_to_html import convert_book

    out = output_dir or BUILD_DIR
    out.mkdir(parents=True, exist_ok=True)

    slug = book_dir.name
    html_path = out / f'{slug}.html'

    # Convert MD → HTML
    print(f"Converting: {book_dir.name}")
    html_content = convert_book(book_dir, css_path=CSS_PATH)
    html_path.write_text(html_content, encoding='utf-8')
    print(f"  HTML: {html_path} ({html_path.stat().st_size // 1024} KB)")

    if not pdf:
        return html_path

    # HTML → PDF via Playwright
    pdf_path = out / f'{slug}.pdf'
    print(f"Rendering PDF...")
    from build_pdf import build_with_playwright
    build_with_playwright([html_path], pdf_path)
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="DOKODU Book Pipeline")
    parser.add_argument('slug', help='Book directory name (slug)')
    parser.add_argument('--html-only', action='store_true', help='Generate HTML only, no PDF')
    parser.add_argument('--preview', action='store_true', help='Open PDF after build')
    parser.add_argument('--books-dir', type=Path, default=BOOKS_DIR,
                        help=f'Books directory (default: {BOOKS_DIR})')
    args = parser.parse_args()

    book_dir = args.books_dir / args.slug
    if not book_dir.exists():
        print(f"Error: Book directory not found: {book_dir}")
        sys.exit(1)

    result = build_book(book_dir, pdf=not args.html_only)

    if args.preview and result.suffix == '.pdf':
        import subprocess
        subprocess.run(['xdg-open', str(result)], check=False)

    print(f"Done! Output: {result}")


if __name__ == '__main__':
    main()
