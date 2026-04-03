"""AI engine: Claude API for field detection in tender documents."""
import json
from pathlib import Path
from docx import Document
import anthropic
from ..models import CompanyProfile, FieldResult, FieldSource, Confidence

_TIMEOUT = 30


def _extract_doc_text(docx_path: Path) -> str:
    doc = Document(str(docx_path))
    parts = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            parts.append(f"[P{i}] {text}")
    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            cells = [c.text.strip() for c in row.cells]
            parts.append(f"[T{t_idx}R{r_idx}] {' | '.join(cells)}")
    return "\n".join(parts)


def _build_prompt(doc_text: str, profile: CompanyProfile, filename: str) -> str:
    profile_json = json.dumps(profile.model_dump(), ensure_ascii=False, indent=2)
    return f"""Analizujesz formularz przetargowy "{filename}".

Profil firmy wykonawcy:
{profile_json}

Treść dokumentu (z oznaczeniami pozycji):
[P0] = paragraf o indeksie 0
[T0R3] = tabela 0, wiersz 3
---
{doc_text}
---

Znajdź WSZYSTKIE pola w dokumencie, które powinny być wypełnione danymi wykonawcy.
Pola to: puste komórki tabel obok etykiet, wielokropki, kropki, puste nawiasy, pola opisane w nawiasach pod nimi.

Dla każdego pola zwróć obiekt JSON z polami:
- "location_id": "T0R3" lub "P13"
- "location_type": "table_cell" lub "paragraph"
- "label": etykieta pola
- "current_value": co jest teraz w polu
- "suggested_value": wartość z profilu firmy
- "confidence": "high", "medium" lub "low"

Zwróć TYLKO tablicę JSON. Nie dodawaj pól, dla których nie ma danych w profilu."""


_EXTRACT_FIELDS_TOOL = {
    "name": "extract_fields",
    "description": "Return all detected company fields from the tender document.",
    "input_schema": {
        "type": "object",
        "properties": {
            "fields": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "location_id": {"type": "string", "description": "e.g. T0R3 or P13"},
                        "location_type": {"type": "string", "enum": ["table_cell", "paragraph"]},
                        "label": {"type": "string"},
                        "current_value": {"type": "string"},
                        "suggested_value": {"type": "string"},
                        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    },
                    "required": ["location_id", "location_type", "label", "suggested_value", "confidence"],
                },
            }
        },
        "required": ["fields"],
    },
}


def _call_claude(prompt: str) -> list[dict]:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        timeout=_TIMEOUT,
        tools=[_EXTRACT_FIELDS_TOOL],
        tool_choice={"type": "tool", "name": "extract_fields"},
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "tool_use" and block.name == "extract_fields":
            return block.input.get("fields", [])
    return []


def analyze_ai(docx_path: Path, profile: CompanyProfile) -> list[FieldResult]:
    """Analyze DOCX using Claude AI and return detected fields."""
    try:
        doc_text = _extract_doc_text(docx_path)
        filename = Path(docx_path).name
        prompt = _build_prompt(doc_text, profile, filename)
        raw_fields = _call_claude(prompt)
    except Exception:
        return []

    results = []
    for f in raw_fields:
        try:
            results.append(FieldResult(
                location_id=f["location_id"],
                location_type=f.get("location_type", "paragraph"),
                label=f["label"],
                original_value=f.get("current_value", ""),
                filled_value=f["suggested_value"],
                source=FieldSource.AI,
                confidence=Confidence(f.get("confidence", "medium")),
            ))
        except (KeyError, ValueError):
            continue
    return results
