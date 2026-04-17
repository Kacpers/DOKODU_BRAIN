"""Tests for book pipeline component renderers."""
import pytest
from renderers import render_component


def test_callout_tip():
    result = render_component('callout', 'tip\nThis is a tip.')
    assert 'class="callout tip"' in result
    assert 'This is a tip.' in result


def test_callout_trap():
    result = render_component('callout', 'trap\nWatch out!')
    assert 'class="callout danger"' in result
    assert 'UWAGA NA PULAPKE' in result.upper() or 'Watch out!' in result


def test_stats():
    result = render_component('stats', '67% | firm wdraza AI\n3x | szybciej')
    assert 'stat-grid' in result
    assert 'stat-box' in result
    assert '67%' in result
    assert 'firm wdraza AI' in result


def test_tiles_2col():
    result = render_component('tiles', '2\nAnaliza | Raporty\nCRM | Integracje')
    assert 'cols-2' in result
    assert 'tile-title' in result
    assert 'Analiza' in result


def test_quote_with_author():
    result = render_component('quote', 'AI zmieni swiat.\n--- Kacper Sieradzinski')
    assert 'quote-block' in result
    assert 'quote-author' in result
    assert 'Kacper' in result


def test_process():
    result = render_component('process', 'Start | Begin\nEnd | Finish')
    assert 'process-flow' in result
    assert 'process-step' in result
    assert 'Start' in result


def test_timeline():
    result = render_component('timeline', '2024 | GPT-4 | Multimodal AI')
    assert 'timeline' in result
    assert 'timeline-item' in result
    assert '2024' in result


def test_info():
    result = render_component('info', 'LLM\nLarge Language Model to...')
    assert 'info-box' in result
    assert 'info-term' in result
    assert 'LLM' in result


def test_summary():
    result = render_component('summary', 'AI jest wazne\nTrzeba wdrazac')
    assert 'chapter-summary' in result
    assert 'summary-title' in result


def test_exercise():
    result = render_component('exercise', 'Otworz ChatGPT i wpisz...')
    assert 'exercise-box' in result


def test_checklist():
    result = render_component('checklist', 'Konto OpenAI\nKlucz API\nPrzegladarka')
    assert 'checklist' in result
    assert result.count('<li>') == 3


def test_prerequisites():
    result = render_component('prerequisites', 'Python 3.10+\nKonto OpenAI')
    assert 'prerequisites-box' in result
    assert 'Python 3.10+' in result


def test_highlight():
    result = render_component('highlight', 'Wazna informacja!')
    assert 'highlight-bar' in result
    assert 'Wazna informacja!' in result


def test_pullquote():
    result = render_component('pullquote', 'AI to nie przyszlosc — to terazniejszosc.')
    assert 'pull-quote' in result


def test_beforeafter():
    result = render_component('beforeafter', 'Reczne raporty co tydzien\n---\nAutomatyczne raporty codziennie')
    assert 'before-after' in result
    assert 'ba-before' in result
    assert 'ba-after' in result


def test_decision():
    result = render_component('decision', 'Czy masz dane?\nTAK | Uzyj RAG\nNIE | Zacznij od fine-tuningu')
    assert 'decision-tree' in result
    assert 'dt-question' in result
    assert 'dt-yes' in result
    assert 'dt-no' in result


def test_code_python():
    result = render_component('code', 'python\nprint("hello")')
    assert 'code-block' in result
    assert 'code-header' in result
    assert 'PYTHON' in result.upper()


def test_unknown_component():
    result = render_component('nonexistent', 'some content')
    assert '<p>' in result  # fallback to paragraph


def test_empty_content():
    result = render_component('callout', 'tip\n')
    assert 'callout' in result
