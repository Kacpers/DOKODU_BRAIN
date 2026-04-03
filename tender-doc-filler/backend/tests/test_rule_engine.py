import pytest
from backend.engines.rule_engine import analyze_rules
from backend.models import FieldResult, FieldSource, Confidence


def test_table_cell_fill(simple_table_docx, sample_profile):
    """Rule engine fills table cells with matching labels."""
    results = analyze_rules(simple_table_docx, sample_profile)
    labels = {r.label.lower() for r in results}
    assert "firma" in labels
    assert "nip" in labels
    assert "adres" in labels
    assert "e-mail" in labels
    for r in results:
        assert r.source == FieldSource.RULE
        assert r.confidence == Confidence.HIGH


def test_paragraph_dots_fill(paragraph_dots_docx, sample_profile):
    """Rule engine fills paragraph fields with dots/ellipsis."""
    results = analyze_rules(paragraph_dots_docx, sample_profile)
    labels_lower = {r.label.lower() for r in results}
    assert "nip" in labels_lower
    assert "tel" in labels_lower or "telefon" in labels_lower


def test_returns_field_result_type(simple_table_docx, sample_profile):
    results = analyze_rules(simple_table_docx, sample_profile)
    assert len(results) > 0
    assert all(isinstance(r, FieldResult) for r in results)


def test_empty_document(tmp_path, sample_profile):
    """Empty doc returns no results."""
    from docx import Document
    doc = Document()
    doc.add_paragraph("No fields here.")
    path = tmp_path / "empty.docx"
    doc.save(path)
    results = analyze_rules(path, sample_profile)
    assert results == []
