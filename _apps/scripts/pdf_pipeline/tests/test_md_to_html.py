"""Integration tests for md_to_html converter."""
import pytest
import tempfile
from pathlib import Path
from md_to_html import convert_book


@pytest.fixture
def book_dir(tmp_path):
    """Create a minimal test book."""
    # book.yaml
    (tmp_path / 'book.yaml').write_text(
        'title: Test Book\n'
        'subtitle: A test\n'
        'author: Tester\n'
        'author_role: QA\n'
        'brand: TEST\n'
        'version: "1.0"\n'
        'date: "2026"\n'
        'cover: dark\n'
        'auto_sections:\n'
        '  how_to_read: true\n'
        '  glossary: true\n'
        '  legal: true\n',
        encoding='utf-8'
    )
    # Chapter 1
    (tmp_path / '01_intro.md').write_text(
        '---\n'
        'chapter: 1\n'
        'title: Intro\n'
        'subtitle: Getting started\n'
        'reading_time: 5 min\n'
        '---\n\n'
        '## First Section\n\n'
        'Some text here.\n\n'
        ':::callout tip\n'
        'This is a tip.\n'
        ':::\n\n'
        ':::info\n'
        'LLM\n'
        'Large Language Model\n'
        ':::\n\n'
        '## Second Section\n\n'
        'More text.\n',
        encoding='utf-8'
    )
    return tmp_path


def test_convert_produces_html(book_dir):
    html = convert_book(book_dir)
    assert '<html' in html
    assert 'Test Book' in html


def test_convert_has_cover(book_dir):
    html = convert_book(book_dir)
    assert 'cover-page' in html


def test_convert_has_legal(book_dir):
    html = convert_book(book_dir)
    assert 'legal-page' in html


def test_convert_has_toc(book_dir):
    html = convert_book(book_dir)
    assert 'toc-page' in html
    assert 'Intro' in html


def test_convert_has_chapter_opener(book_dir):
    html = convert_book(book_dir)
    assert 'chapter-opener' in html
    assert 'Rozdzial 1' in html


def test_convert_has_mini_toc(book_dir):
    html = convert_book(book_dir)
    assert 'mini-toc' in html
    assert 'First Section' in html


def test_convert_has_drop_cap(book_dir):
    html = convert_book(book_dir)
    assert 'drop-cap' in html


def test_convert_has_components(book_dir):
    html = convert_book(book_dir)
    assert 'callout tip' in html
    assert 'info-box' in html


def test_convert_collects_glossary(book_dir):
    html = convert_book(book_dir)
    assert 'glossary-page' in html
    assert 'LLM' in html


def test_convert_has_how_to_read(book_dir):
    html = convert_book(book_dir)
    assert 'how-to-read' in html
