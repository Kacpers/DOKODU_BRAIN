"""End-to-end test for build_book orchestrator."""
import pytest
from pathlib import Path
from build_book import build_book


@pytest.fixture
def test_book(tmp_path):
    """Create minimal test book."""
    (tmp_path / 'book.yaml').write_text(
        'title: E2E Test\nsubtitle: Test\nauthor: Bot\n'
        'author_role: QA\nbrand: TEST\ncover: dark\n'
        'version: "1.0"\ndate: "2026"\n'
        'auto_sections:\n  legal: true\n',
        encoding='utf-8'
    )
    (tmp_path / '01_test.md').write_text(
        '---\nchapter: 1\ntitle: Test Chapter\n---\n\n'
        'Hello world.\n',
        encoding='utf-8'
    )
    return tmp_path


def test_build_generates_html(test_book, tmp_path):
    """Test that build produces an HTML file."""
    output = tmp_path / 'output'
    output.mkdir()
    html_path = build_book(test_book, output_dir=output, pdf=False)
    assert html_path.exists()
    assert html_path.suffix == '.html'
    content = html_path.read_text()
    assert 'E2E Test' in content
    assert 'Test Chapter' in content
