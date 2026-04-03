import pytest
from unittest.mock import patch
from backend.engines.ai_engine import analyze_ai, _extract_doc_text
from backend.models import FieldResult


def test_extract_doc_text(simple_table_docx):
    text = _extract_doc_text(simple_table_docx)
    assert "[T0R0]" in text
    assert "Firma" in text
    assert "NIP" in text


def test_extract_doc_text_paragraphs(paragraph_dots_docx):
    text = _extract_doc_text(paragraph_dots_docx)
    assert "[P0]" in text
    assert "FORMULARZ" in text


MOCK_AI_RESPONSE = [
    {
        "location_id": "P1",
        "location_type": "paragraph",
        "label": "nazwa Wykonawcy",
        "current_value": "............",
        "suggested_value": "TestFirma Sp. z o.o.",
        "confidence": "high",
    },
    {
        "location_id": "P3",
        "location_type": "paragraph",
        "label": "tel.",
        "current_value": "...........",
        "suggested_value": "+48 111 222 333",
        "confidence": "medium",
    },
]


@patch("backend.engines.ai_engine._call_claude")
def test_analyze_ai_returns_fields(mock_claude, paragraph_dots_docx, sample_profile):
    mock_claude.return_value = MOCK_AI_RESPONSE
    results = analyze_ai(paragraph_dots_docx, sample_profile)
    assert len(results) == 2
    assert all(isinstance(r, FieldResult) for r in results)


@patch("backend.engines.ai_engine._call_claude")
def test_analyze_ai_handles_error(mock_claude, paragraph_dots_docx, sample_profile):
    mock_claude.side_effect = Exception("API error")
    with pytest.raises(Exception):
        analyze_ai(paragraph_dots_docx, sample_profile)
