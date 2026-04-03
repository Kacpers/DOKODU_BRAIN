# TenderScope Document Filler — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Working MVP webapp that auto-fills company data in Polish tender DOCX forms, deployed to tender-demo.dokodu.it by 09.04.2026.

**Architecture:** FastAPI backend with two engines (rule-based regex/table matching + Claude AI fallback). Next.js frontend as single-page app with upload, preview, and download. Single Docker deployment behind nginx.

**Tech Stack:** Python 3.11, FastAPI, python-docx, anthropic SDK, Next.js 14, React, TypeScript, Tailwind CSS, Docker

**Spec:** `docs/superpowers/specs/2026-04-03-tender-doc-filler-design.md`

**POC reference:** `scripts/tender_poc/poc_rule_based.py` (working rule engine, tested on 7 real documents)

**Test documents:** `/mnt/d/DOWNLOAD/reprobaowycenwykonaniemoduuuzupenianiadanychw/` (7 DOCX files from TenderScope)

---

## File Structure

```
tender-doc-filler/
├── backend/
│   ├── main.py                  # FastAPI app, endpoints, file handling
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── rule_engine.py       # Table + paragraph regex matching
│   │   ├── ai_engine.py         # Claude API integration
│   │   └── hybrid.py            # Orchestrates rule → AI fallback
│   ├── docx_writer.py           # Write-back filled values to DOCX
│   ├── models.py                # Pydantic schemas (FieldResult, Profile, etc.)
│   ├── profile.py               # Load/save profile JSON
│   ├── requirements.txt
│   └── default_profile.json     # Pre-filled company profile
├── backend/tests/
│   ├── conftest.py              # Fixtures: sample DOCX, profile
│   ├── test_rule_engine.py
│   ├── test_ai_engine.py
│   ├── test_docx_writer.py
│   ├── test_api.py
│   └── fixtures/                # Minimal test DOCX files
│       ├── simple_table.docx
│       └── paragraph_dots.docx
├── frontend/
│   ├── src/app/
│   │   ├── layout.tsx
│   │   └── page.tsx             # Main SPA page
│   ├── src/components/
│   │   ├── Upload.tsx           # Drag & drop upload
│   │   ├── FieldPreview.tsx     # Color-coded field list
│   │   ├── ProfileCard.tsx      # Editable company profile
│   │   └── ModeToggle.tsx       # Rule/AI/Hybrid switch
│   ├── src/lib/
│   │   └── api.ts               # API client functions
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.js
├── Dockerfile
├── nginx.conf
└── README.md
```

---

## Task 1: Project Scaffold + Models

**Files:**
- Create: `tender-doc-filler/backend/models.py`
- Create: `tender-doc-filler/backend/default_profile.json`
- Create: `tender-doc-filler/backend/profile.py`
- Create: `tender-doc-filler/backend/requirements.txt`
- Create: `tender-doc-filler/backend/engines/__init__.py`
- Create: `tender-doc-filler/backend/tests/conftest.py`

- [ ] **Step 1: Create project directory structure**

```bash
mkdir -p tender-doc-filler/backend/engines tender-doc-filler/backend/tests/fixtures tender-doc-filler/frontend
```

- [ ] **Step 2: Write requirements.txt**

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-docx==1.1.2
python-multipart==0.0.9
anthropic==0.40.0
pydantic==2.9.0
pytest==8.3.0
httpx==0.27.0
```

- [ ] **Step 3: Write Pydantic models**

Create `backend/models.py`:

```python
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel


class AnalysisMode(str, Enum):
    RULE = "rule"
    AI = "ai"
    HYBRID = "hybrid"


class FieldSource(str, Enum):
    RULE = "rule"
    AI = "ai"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FieldResult(BaseModel):
    location_id: str          # "T0R3" or "P13"
    location_type: str        # "table_cell" or "paragraph"
    label: str                # human-readable field label
    original_value: str       # what was in the field before
    filled_value: str         # value inserted
    source: FieldSource
    confidence: Confidence


class AnalysisResponse(BaseModel):
    document_id: str
    filename: str
    mode: AnalysisMode
    fields: list[FieldResult]
    total_fields: int
    filled_fields: int


class CompanyProfile(BaseModel):
    nazwa_firmy: str = ""
    nip: str = ""
    regon: str = ""
    krs: str = ""
    adres: str = ""
    adres_korespondencyjny: str = ""
    email: str = ""
    telefon: str = ""
    osoba_kontaktowa: str = ""
    stanowisko: str = ""
    status_przedsiebiorcy: str = ""
    miejscowosc: str = ""


class ErrorResponse(BaseModel):
    error: str
    code: str  # INVALID_FORMAT, NOT_FOUND, AI_FAILED, INTERNAL
```

- [ ] **Step 4: Write default_profile.json**

```json
{
    "nazwa_firmy": "Przykładowa Firma Sp. z o.o.",
    "nip": "1234567890",
    "regon": "123456789",
    "krs": "0000123456",
    "adres": "ul. Przykładowa 1, 00-001 Warszawa",
    "adres_korespondencyjny": "ul. Przykładowa 1, 00-001 Warszawa",
    "email": "biuro@firma.pl",
    "telefon": "+48 123 456 789",
    "osoba_kontaktowa": "Jan Kowalski",
    "stanowisko": "Prezes Zarządu",
    "status_przedsiebiorcy": "mikro",
    "miejscowosc": "Warszawa"
}
```

- [ ] **Step 5: Write profile.py**

```python
import json
from pathlib import Path
from .models import CompanyProfile

PROFILE_PATH = Path(__file__).parent / "default_profile.json"


def load_profile() -> CompanyProfile:
    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return CompanyProfile(**data)


def save_profile(profile: CompanyProfile) -> None:
    PROFILE_PATH.write_text(
        json.dumps(profile.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

- [ ] **Step 6: Write engines/__init__.py**

```python
# empty
```

- [ ] **Step 7: Write tests/conftest.py with DOCX fixture builder**

```python
import pytest
from pathlib import Path
from docx import Document


@pytest.fixture
def sample_profile():
    from backend.models import CompanyProfile
    return CompanyProfile(
        nazwa_firmy="TestFirma Sp. z o.o.",
        nip="1111111111",
        regon="222222222",
        krs="0000333333",
        adres="ul. Testowa 5, 00-001 Warszawa",
        adres_korespondencyjny="ul. Testowa 5, 00-001 Warszawa",
        email="test@firma.pl",
        telefon="+48 111 222 333",
        osoba_kontaktowa="Anna Testowa",
        stanowisko="CEO",
        status_przedsiebiorcy="mikro",
        miejscowosc="Warszawa",
    )


@pytest.fixture
def simple_table_docx(tmp_path) -> Path:
    """DOCX with a table containing company fields."""
    doc = Document()
    table = doc.add_table(rows=4, cols=2)
    fields = [("Firma", ""), ("NIP", ""), ("Adres", ""), ("E-mail", "")]
    for i, (label, val) in enumerate(fields):
        table.rows[i].cells[0].text = label
        table.rows[i].cells[1].text = val
    path = tmp_path / "simple_table.docx"
    doc.save(path)
    return path


@pytest.fixture
def paragraph_dots_docx(tmp_path) -> Path:
    """DOCX with paragraph-style fields using dots."""
    doc = Document()
    doc.add_paragraph("FORMULARZ OFERTOWY")
    doc.add_paragraph("NIP: ……………………………………")
    doc.add_paragraph("tel.: .....................................................")
    doc.add_paragraph("e-mail: ................................................")
    doc.add_paragraph("Łącznie brutto ……………………... PLN")
    path = tmp_path / "paragraph_dots.docx"
    doc.save(path)
    return path
```

- [ ] **Step 8: Install deps and verify**

```bash
cd tender-doc-filler && pip install -r backend/requirements.txt
```

- [ ] **Step 9: Commit**

```bash
git add tender-doc-filler/
git commit -m "feat: project scaffold — models, profile, test fixtures"
```

---

## Task 2: Rule Engine

**Files:**
- Create: `tender-doc-filler/backend/engines/rule_engine.py`
- Create: `tender-doc-filler/backend/tests/test_rule_engine.py`

Port from working POC at `scripts/tender_poc/poc_rule_based.py` but refactored to use `CompanyProfile` model and return `FieldResult` objects.

- [ ] **Step 1: Write failing tests**

Create `backend/tests/test_rule_engine.py`:

```python
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
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_rule_engine.py -v
```

Expected: ImportError — `rule_engine` module does not exist yet.

- [ ] **Step 3: Implement rule_engine.py**

Create `backend/engines/rule_engine.py`:

```python
"""Rule-based engine: regex + table cell matching for known company fields."""
import re
from pathlib import Path
from docx import Document
from ..models import CompanyProfile, FieldResult, FieldSource, Confidence


def _build_label_map(profile: CompanyProfile) -> dict[str, str]:
    """Map normalized label strings to profile values."""
    p = profile
    entries = {
        "firma": p.nazwa_firmy,
        "nazwa": p.nazwa_firmy,
        "nazwa firmy": p.nazwa_firmy,
        "nazwa wykonawcy": p.nazwa_firmy,
        "nazwa oferenta": p.nazwa_firmy,
        "nip": p.nip,
        "regon": p.regon,
        "krs": p.krs,
        "adres": p.adres,
        "adres wykonawcy": p.adres,
        "adres do korespondencji": p.adres_korespondencyjny,
        "adres korespondencyjny": p.adres_korespondencyjny,
        "adres e-mail": p.email,
        "e-mail": p.email,
        "email": p.email,
        "telefon": p.telefon,
        "tel": p.telefon,
        "numer telefonu": p.telefon,
        "osoba do kontaktu": p.osoba_kontaktowa,
        "osoba do kontaktu\n(imię i nazwisko)": p.osoba_kontaktowa,
        "status przedsiębiorcy": p.status_przedsiebiorcy,
        "wielkość przedsiębiorstwa": p.status_przedsiebiorcy,
        "miejscowość i data": f"{p.miejscowosc}, {__import__('datetime').date.today().strftime('%d.%m.%Y')}",
    }
    return {k: v for k, v in entries.items() if v}


def _normalize_label(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r'[:\*]+$', '', t).strip()
    t = re.sub(r'\s+', ' ', t)
    return t


def _is_empty_value(text: str) -> bool:
    stripped = text.strip()
    return (
        stripped == ""
        or bool(re.match(r'^[…\.]+$', stripped))
        or "mikro/małe/średnie/duże" in stripped
        or "niepotrzebne skreślić" in stripped.lower()
    )


def _scan_tables(doc: Document, label_map: dict[str, str]) -> list[FieldResult]:
    results = []
    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            cells = row.cells
            if len(cells) < 2:
                continue
            label_raw = cells[0].text.strip()
            value_raw = cells[1].text.strip()
            label_norm = _normalize_label(label_raw)
            if label_norm in label_map and _is_empty_value(value_raw):
                results.append(FieldResult(
                    location_id=f"T{t_idx}R{r_idx}",
                    location_type="table_cell",
                    label=label_raw,
                    original_value=value_raw,
                    filled_value=label_map[label_norm],
                    source=FieldSource.RULE,
                    confidence=Confidence.HIGH,
                ))
    return results


def _scan_paragraphs(doc: Document, label_map: dict[str, str]) -> list[FieldResult]:
    results = []
    for p_idx, para in enumerate(doc.paragraphs):
        text = para.text
        match = re.search(r'([\w\s]+?)\s*[:]*\s*([…\.]{3,})', text)
        if match:
            label_norm = _normalize_label(match.group(1))
            if label_norm in label_map:
                results.append(FieldResult(
                    location_id=f"P{p_idx}",
                    location_type="paragraph",
                    label=match.group(1).strip(),
                    original_value=match.group(2),
                    filled_value=label_map[label_norm],
                    source=FieldSource.RULE,
                    confidence=Confidence.HIGH,
                ))
    return results


def analyze_rules(docx_path: Path, profile: CompanyProfile) -> list[FieldResult]:
    """Analyze DOCX and return fields that can be filled by rules."""
    doc = Document(str(docx_path))
    label_map = _build_label_map(profile)
    table_results = _scan_tables(doc, label_map)
    para_results = _scan_paragraphs(doc, label_map)
    return table_results + para_results
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_rule_engine.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Validate on real TenderScope documents**

```bash
cd tender-doc-filler && python -c "
from pathlib import Path
from backend.engines.rule_engine import analyze_rules
from backend.models import CompanyProfile

profile = CompanyProfile(nazwa_firmy='DOKODU Sp. z o.o.', nip='5882473305', regon='520149113', krs='0000925166', adres='ul. Kosynierów 76/22, 84-230 Rumia', adres_korespondencyjny='ul. Kosynierów 76/22, 84-230 Rumia', email='biuro@dokodu.it', telefon='+48 508 106 046', osoba_kontaktowa='Kacper Sieradziński', stanowisko='CEO', status_przedsiebiorcy='mikro', miejscowosc='Rumia')
folder = Path('/mnt/d/DOWNLOAD/reprobaowycenwykonaniemoduuuzupenianiadanychw')
for f in sorted(folder.glob('*.docx')):
    results = analyze_rules(f, profile)
    print(f'{f.name}: {len(results)} fields')
    for r in results:
        print(f'  [{r.location_id}] {r.label} -> {r.filled_value}')
"
```

Expected: Same 24 fields as POC.

- [ ] **Step 6: Commit**

```bash
git add tender-doc-filler/backend/engines/rule_engine.py tender-doc-filler/backend/tests/test_rule_engine.py
git commit -m "feat: rule engine — table + paragraph matching"
```

---

## Task 3: AI Engine

**Files:**
- Create: `tender-doc-filler/backend/engines/ai_engine.py`
- Create: `tender-doc-filler/backend/tests/test_ai_engine.py`

- [ ] **Step 1: Write tests (with mock for Claude API)**

Create `backend/tests/test_ai_engine.py`:

```python
import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
from backend.engines.ai_engine import analyze_ai, _extract_doc_text
from backend.models import FieldResult, FieldSource


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
    assert all(r.source == FieldSource.AI for r in results)


@patch("backend.engines.ai_engine._call_claude")
def test_analyze_ai_timeout(mock_claude, paragraph_dots_docx, sample_profile):
    mock_claude.side_effect = TimeoutError("Claude timeout")
    results = analyze_ai(paragraph_dots_docx, sample_profile)
    assert results == []
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_ai_engine.py -v
```

- [ ] **Step 3: Implement ai_engine.py**

Create `backend/engines/ai_engine.py`:

```python
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
Pola to: puste komórki tabel obok etykiet, wielokropki (……), kropki (......), puste nawiasy, pola opisane w nawiasach pod nimi.

Dla każdego pola zwróć obiekt JSON z polami:
- "location_id": "T0R3" lub "P13"
- "location_type": "table_cell" lub "paragraph"
- "label": etykieta pola
- "current_value": co jest teraz w polu
- "suggested_value": wartość z profilu firmy
- "confidence": "high", "medium" lub "low"

Zwróć TYLKO tablicę JSON. Nie dodawaj pól, dla których nie ma danych w profilu (np. cena, specyfikacja techniczna)."""


def _call_claude(prompt: str) -> list[dict]:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        timeout=_TIMEOUT,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


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
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_ai_engine.py -v
```

- [ ] **Step 5: Commit**

```bash
git add tender-doc-filler/backend/engines/ai_engine.py tender-doc-filler/backend/tests/test_ai_engine.py
git commit -m "feat: AI engine — Claude-powered field detection"
```

---

## Task 4: Hybrid Engine + DOCX Writer

**Files:**
- Create: `tender-doc-filler/backend/engines/hybrid.py`
- Create: `tender-doc-filler/backend/docx_writer.py`
- Create: `tender-doc-filler/backend/tests/test_docx_writer.py`

- [ ] **Step 1: Write hybrid.py**

```python
"""Hybrid engine: rules first, AI fallback for unfilled fields."""
from pathlib import Path
from ..models import CompanyProfile, FieldResult, AnalysisMode
from .rule_engine import analyze_rules
from .ai_engine import analyze_ai


def analyze(docx_path: Path, profile: CompanyProfile, mode: AnalysisMode) -> list[FieldResult]:
    if mode == AnalysisMode.RULE:
        return analyze_rules(docx_path, profile)

    if mode == AnalysisMode.AI:
        return analyze_ai(docx_path, profile)

    # HYBRID: rules first, then AI for additional fields
    rule_results = analyze_rules(docx_path, profile)
    rule_locations = {r.location_id for r in rule_results}
    ai_results = analyze_ai(docx_path, profile)
    # Only add AI results for locations not already found by rules
    additional = [r for r in ai_results if r.location_id not in rule_locations]
    return rule_results + additional
```

- [ ] **Step 2: Write tests for docx_writer**

Create `backend/tests/test_docx_writer.py`:

```python
import pytest
from pathlib import Path
from docx import Document
from backend.docx_writer import write_fields
from backend.models import FieldResult, FieldSource, Confidence


def test_write_table_cell(simple_table_docx, tmp_path):
    fields = [
        FieldResult(
            location_id="T0R0", location_type="table_cell", label="Firma",
            original_value="", filled_value="Test Corp",
            source=FieldSource.RULE, confidence=Confidence.HIGH,
        ),
        FieldResult(
            location_id="T0R1", location_type="table_cell", label="NIP",
            original_value="", filled_value="1234567890",
            source=FieldSource.RULE, confidence=Confidence.HIGH,
        ),
    ]
    out_path = tmp_path / "filled.docx"
    write_fields(simple_table_docx, fields, out_path)
    doc = Document(str(out_path))
    assert doc.tables[0].rows[0].cells[1].text.strip() == "Test Corp"
    assert doc.tables[0].rows[1].cells[1].text.strip() == "1234567890"


def test_write_paragraph_dots(paragraph_dots_docx, tmp_path):
    fields = [
        FieldResult(
            location_id="P1", location_type="paragraph", label="NIP",
            original_value="……………………………………", filled_value="1234567890",
            source=FieldSource.RULE, confidence=Confidence.HIGH,
        ),
    ]
    out_path = tmp_path / "filled.docx"
    write_fields(paragraph_dots_docx, fields, out_path)
    doc = Document(str(out_path))
    assert "1234567890" in doc.paragraphs[1].text
    assert "……" not in doc.paragraphs[1].text
```

- [ ] **Step 3: Run tests, verify they fail**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_docx_writer.py -v
```

- [ ] **Step 4: Implement docx_writer.py**

```python
"""Write filled values back into DOCX preserving formatting."""
import re
from pathlib import Path
from docx import Document
from .models import FieldResult


def _parse_table_location(loc_id: str) -> tuple[int, int] | None:
    m = re.match(r"T(\d+)R(\d+)", loc_id)
    return (int(m.group(1)), int(m.group(2))) if m else None


def _parse_paragraph_location(loc_id: str) -> int | None:
    m = re.match(r"P(\d+)", loc_id)
    return int(m.group(1)) if m else None


def _replace_dots_in_runs(paragraph, value: str) -> bool:
    """Replace dots/ellipsis in paragraph runs, preserving formatting."""
    for run in paragraph.runs:
        if re.search(r'[…\.]{3,}', run.text):
            run.text = re.sub(r'[…\.]{3,}', value, run.text)
            return True
    # Fallback: replace in full paragraph text
    if re.search(r'[…\.]{3,}', paragraph.text):
        paragraph.text = re.sub(r'[…\.]{3,}', value, paragraph.text)
        return True
    # Last resort: if paragraph is empty or only whitespace, set text
    if not paragraph.text.strip():
        if paragraph.runs:
            paragraph.runs[0].text = value
        else:
            paragraph.text = value
        return True
    return False


def write_fields(source_path: Path, fields: list[FieldResult], output_path: Path) -> None:
    """Write field values into DOCX and save to output_path."""
    doc = Document(str(source_path))

    for field in fields:
        if field.location_type == "table_cell":
            loc = _parse_table_location(field.location_id)
            if loc:
                t_idx, r_idx = loc
                try:
                    cell = doc.tables[t_idx].rows[r_idx].cells[1]
                    if cell.paragraphs:
                        cell.paragraphs[0].text = field.filled_value
                    else:
                        cell.text = field.filled_value
                except (IndexError, KeyError):
                    continue

        elif field.location_type == "paragraph":
            p_idx = _parse_paragraph_location(field.location_id)
            if p_idx is not None:
                try:
                    para = doc.paragraphs[p_idx]
                    _replace_dots_in_runs(para, field.filled_value)
                except IndexError:
                    continue

    doc.save(str(output_path))
```

- [ ] **Step 5: Run tests, verify they pass**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_docx_writer.py -v
```

- [ ] **Step 6: Commit**

```bash
git add tender-doc-filler/backend/engines/hybrid.py tender-doc-filler/backend/docx_writer.py tender-doc-filler/backend/tests/test_docx_writer.py
git commit -m "feat: hybrid engine + DOCX writer with format preservation"
```

---

## Task 5: FastAPI Backend

**Files:**
- Create: `tender-doc-filler/backend/main.py`
- Create: `tender-doc-filler/backend/tests/test_api.py`

- [ ] **Step 1: Write API tests**

Create `backend/tests/test_api.py`:

```python
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def uploaded_doc(client, simple_table_docx):
    with open(simple_table_docx, "rb") as f:
        resp = client.post("/api/upload", files={"file": ("test.docx", f)}, params={"mode": "rule"})
    assert resp.status_code == 200
    return resp.json()


def test_upload_docx(client, simple_table_docx):
    with open(simple_table_docx, "rb") as f:
        resp = client.post("/api/upload", files={"file": ("test.docx", f)}, params={"mode": "rule"})
    assert resp.status_code == 200
    data = resp.json()
    assert "document_id" in data
    assert data["filled_fields"] > 0


def test_upload_invalid_format(client, tmp_path):
    txt = tmp_path / "test.txt"
    txt.write_text("not a docx")
    with open(txt, "rb") as f:
        resp = client.post("/api/upload", files={"file": ("test.txt", f)})
    assert resp.status_code == 400
    assert resp.json()["code"] == "INVALID_FORMAT"


def test_get_document(client, uploaded_doc):
    doc_id = uploaded_doc["document_id"]
    resp = client.get(f"/api/documents/{doc_id}")
    assert resp.status_code == 200
    assert resp.json()["document_id"] == doc_id


def test_get_document_not_found(client):
    resp = client.get("/api/documents/nonexistent-uuid")
    assert resp.status_code == 404


def test_download_filled(client, uploaded_doc):
    doc_id = uploaded_doc["document_id"]
    resp = client.get(f"/api/documents/{doc_id}/download")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def test_get_profile(client):
    resp = client.get("/api/profile")
    assert resp.status_code == 200
    assert "nazwa_firmy" in resp.json()


def test_update_profile(client):
    resp = client.put("/api/profile", json={"nazwa_firmy": "Updated Corp", "nip": "999"})
    assert resp.status_code == 200
    resp2 = client.get("/api/profile")
    assert resp2.json()["nazwa_firmy"] == "Updated Corp"
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_api.py -v
```

- [ ] **Step 3: Implement main.py**

```python
"""FastAPI app for TenderScope Document Filler."""
import uuid
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import FileResponse
from .models import AnalysisMode, AnalysisResponse, CompanyProfile, ErrorResponse
from .engines.hybrid import analyze
from .docx_writer import write_fields
from .profile import load_profile, save_profile

app = FastAPI(title="TenderScope Document Filler", version="0.1.0")

UPLOAD_DIR = Path("/tmp/tender")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# In-memory store for analysis results
_results: dict[str, AnalysisResponse] = {}


@app.post("/api/upload", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    mode: AnalysisMode = Query(default=AnalysisMode.HYBRID),
):
    if not file.filename or not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail=ErrorResponse(
            error="Only .docx files are supported", code="INVALID_FORMAT"
        ).model_dump())

    doc_id = str(uuid.uuid4())
    doc_dir = UPLOAD_DIR / doc_id
    doc_dir.mkdir(parents=True, exist_ok=True)

    source_path = doc_dir / file.filename
    with open(source_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    profile = load_profile()
    fields = analyze(source_path, profile, mode)

    # Write filled document
    filled_path = doc_dir / f"FILLED_{file.filename}"
    write_fields(source_path, fields, filled_path)

    response = AnalysisResponse(
        document_id=doc_id,
        filename=file.filename,
        mode=mode,
        fields=fields,
        total_fields=len(fields),
        filled_fields=len([f for f in fields if f.filled_value]),
    )
    _results[doc_id] = response
    return response


@app.get("/api/documents/{doc_id}", response_model=AnalysisResponse)
async def get_document(doc_id: str):
    if doc_id not in _results:
        raise HTTPException(status_code=404, detail=ErrorResponse(
            error="Document not found", code="NOT_FOUND"
        ).model_dump())
    return _results[doc_id]


@app.get("/api/documents/{doc_id}/download")
async def download_filled(doc_id: str):
    if doc_id not in _results:
        raise HTTPException(status_code=404, detail=ErrorResponse(
            error="Document not found", code="NOT_FOUND"
        ).model_dump())
    doc_dir = UPLOAD_DIR / doc_id
    filled_files = list(doc_dir.glob("FILLED_*"))
    if not filled_files:
        raise HTTPException(status_code=404, detail=ErrorResponse(
            error="Filled document not found", code="NOT_FOUND"
        ).model_dump())
    return FileResponse(
        filled_files[0],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filled_files[0].name,
    )


@app.get("/api/profile", response_model=CompanyProfile)
async def get_profile():
    return load_profile()


@app.put("/api/profile", response_model=CompanyProfile)
async def update_profile(profile: CompanyProfile):
    save_profile(profile)
    return profile
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
cd tender-doc-filler && python -m pytest backend/tests/test_api.py -v
```

- [ ] **Step 5: Manual smoke test**

```bash
cd tender-doc-filler && uvicorn backend.main:app --reload --port 8000
# In another terminal:
curl -X POST "http://localhost:8000/api/upload?mode=rule" -F "file=@/mnt/d/DOWNLOAD/reprobaowycenwykonaniemoduuuzupenianiadanychw/Zał nr 1 formularz ofertowy.docx"
```

- [ ] **Step 6: Commit**

```bash
git add tender-doc-filler/backend/main.py tender-doc-filler/backend/tests/test_api.py
git commit -m "feat: FastAPI backend — upload, analyze, download endpoints"
```

---

## Task 6: Next.js Frontend

**Files:**
- Create: `tender-doc-filler/frontend/` (full Next.js app)

- [ ] **Step 1: Scaffold Next.js project**

```bash
cd tender-doc-filler && npx create-next-app@14 frontend --typescript --tailwind --app --no-eslint --no-src-dir --import-alias "@/*"
```

Note: adjust if the scaffolder uses different flags. Key: TypeScript + Tailwind + App Router.

- [ ] **Step 2: Write API client**

Create `frontend/lib/api.ts`:

```typescript
const API_BASE = "/api";

export interface FieldResult {
  location_id: string;
  location_type: string;
  label: string;
  original_value: string;
  filled_value: string;
  source: "rule" | "ai";
  confidence: "high" | "medium" | "low";
}

export interface AnalysisResponse {
  document_id: string;
  filename: string;
  mode: string;
  fields: FieldResult[];
  total_fields: number;
  filled_fields: number;
}

export interface CompanyProfile {
  nazwa_firmy: string;
  nip: string;
  regon: string;
  krs: string;
  adres: string;
  adres_korespondencyjny: string;
  email: string;
  telefon: string;
  osoba_kontaktowa: string;
  stanowisko: string;
  status_przedsiebiorcy: string;
  miejscowosc: string;
}

export async function uploadDocument(
  file: File,
  mode: "rule" | "ai" | "hybrid" = "hybrid"
): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const resp = await fetch(`${API_BASE}/upload?mode=${mode}`, {
    method: "POST",
    body: formData,
  });
  if (!resp.ok) throw new Error((await resp.json()).error);
  return resp.json();
}

export async function getProfile(): Promise<CompanyProfile> {
  const resp = await fetch(`${API_BASE}/profile`);
  return resp.json();
}

export async function updateProfile(profile: CompanyProfile): Promise<CompanyProfile> {
  const resp = await fetch(`${API_BASE}/profile`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  return resp.json();
}

export function getDownloadUrl(documentId: string): string {
  return `${API_BASE}/documents/${documentId}/download`;
}
```

- [ ] **Step 3: Write ModeToggle component**

Create `frontend/components/ModeToggle.tsx`:

```tsx
"use client";

type Mode = "rule" | "ai" | "hybrid";

interface ModeToggleProps {
  mode: Mode;
  onChange: (mode: Mode) => void;
}

const MODES: { value: Mode; label: string; description: string }[] = [
  { value: "rule", label: "Regułowy", description: "Regex + tabele, szybki, 100% pewny" },
  { value: "ai", label: "AI", description: "Claude rozpoznaje pola z treści" },
  { value: "hybrid", label: "Hybrydowy", description: "Reguły + AI fallback" },
];

export default function ModeToggle({ mode, onChange }: ModeToggleProps) {
  return (
    <div className="flex gap-2">
      {MODES.map((m) => (
        <button
          key={m.value}
          onClick={() => onChange(m.value)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            mode === m.value
              ? "bg-blue-600 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
          title={m.description}
        >
          {m.label}
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 4: Write Upload component**

Create `frontend/components/Upload.tsx`:

```tsx
"use client";
import { useCallback, useState } from "react";

interface UploadProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

export default function Upload({ onUpload, isLoading }: UploadProps) {
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file?.name.endsWith(".docx")) onUpload(file);
    },
    [onUpload]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) onUpload(file);
    },
    [onUpload]
  );

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
        dragOver ? "border-blue-500 bg-blue-50" : "border-gray-300"
      } ${isLoading ? "opacity-50 pointer-events-none" : ""}`}
    >
      {isLoading ? (
        <div className="text-gray-500">Analizuję dokument...</div>
      ) : (
        <>
          <p className="text-gray-600 mb-4">Przeciągnij plik DOCX lub kliknij aby wybrać</p>
          <label className="cursor-pointer inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Wybierz plik
            <input type="file" accept=".docx" className="hidden" onChange={handleChange} />
          </label>
        </>
      )}
    </div>
  );
}
```

- [ ] **Step 5: Write FieldPreview component**

Create `frontend/components/FieldPreview.tsx`:

```tsx
"use client";
import type { FieldResult } from "@/lib/api";

interface FieldPreviewProps {
  fields: FieldResult[];
  filename: string;
}

function getFieldColor(field: FieldResult): string {
  if (field.source === "rule") return "bg-green-50 border-green-200 text-green-800";
  if (field.confidence === "low") return "bg-red-50 border-red-200 text-red-800";
  return "bg-blue-50 border-blue-200 text-blue-800";
}

function getFieldIcon(field: FieldResult): string {
  if (field.source === "rule") return "🟢";
  if (field.confidence === "low") return "🔴";
  return "🔵";
}

export default function FieldPreview({ fields, filename }: FieldPreviewProps) {
  const ruleCount = fields.filter((f) => f.source === "rule").length;
  const aiCount = fields.filter((f) => f.source === "ai").length;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">{filename}</h2>
        <div className="text-sm text-gray-500">
          Wypełniono {fields.length} pól
          {ruleCount > 0 && <span className="ml-2">🟢 {ruleCount} regułowe</span>}
          {aiCount > 0 && <span className="ml-2">🔵 {aiCount} AI</span>}
        </div>
      </div>
      <div className="space-y-2">
        {fields.map((field, i) => (
          <div key={i} className={`flex items-center gap-3 p-3 rounded-lg border ${getFieldColor(field)}`}>
            <span>{getFieldIcon(field)}</span>
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm">{field.label}</div>
              <div className="text-xs opacity-70">[{field.location_id}]</div>
            </div>
            <div className="text-sm font-mono">{field.filled_value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 6: Write ProfileCard component**

Create `frontend/components/ProfileCard.tsx`:

```tsx
"use client";
import { useState } from "react";
import type { CompanyProfile } from "@/lib/api";

interface ProfileCardProps {
  profile: CompanyProfile;
  onSave: (profile: CompanyProfile) => void;
}

const FIELD_LABELS: Record<string, string> = {
  nazwa_firmy: "Nazwa firmy",
  nip: "NIP",
  regon: "REGON",
  krs: "KRS",
  adres: "Adres",
  adres_korespondencyjny: "Adres korespondencyjny",
  email: "E-mail",
  telefon: "Telefon",
  osoba_kontaktowa: "Osoba kontaktowa",
  stanowisko: "Stanowisko",
  status_przedsiebiorcy: "Status przedsiębiorcy",
  miejscowosc: "Miejscowość",
};

export default function ProfileCard({ profile, onSave }: ProfileCardProps) {
  const [data, setData] = useState<CompanyProfile>(profile);
  const [expanded, setExpanded] = useState(false);

  const handleChange = (key: keyof CompanyProfile, value: string) => {
    setData((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="border rounded-xl p-4 bg-gray-50">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between w-full text-left"
      >
        <h3 className="font-semibold">Profil firmy</h3>
        <span className="text-gray-400">{expanded ? "▲" : "▼"}</span>
      </button>
      {expanded && (
        <div className="mt-4 space-y-3">
          {Object.entries(FIELD_LABELS).map(([key, label]) => (
            <div key={key} className="flex gap-2 items-center">
              <label className="w-48 text-sm text-gray-600 shrink-0">{label}</label>
              <input
                type="text"
                value={data[key as keyof CompanyProfile]}
                onChange={(e) => handleChange(key as keyof CompanyProfile, e.target.value)}
                className="flex-1 px-3 py-1.5 border rounded text-sm"
              />
            </div>
          ))}
          <button
            onClick={() => onSave(data)}
            className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700"
          >
            Zapisz profil
          </button>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 7: Write main page**

Replace `frontend/app/page.tsx`:

```tsx
"use client";
import { useState, useEffect } from "react";
import Upload from "@/components/Upload";
import FieldPreview from "@/components/FieldPreview";
import ProfileCard from "@/components/ProfileCard";
import ModeToggle from "@/components/ModeToggle";
import {
  uploadDocument,
  getProfile,
  updateProfile,
  getDownloadUrl,
  type AnalysisResponse,
  type CompanyProfile,
} from "@/lib/api";

type Mode = "rule" | "ai" | "hybrid";

export default function Home() {
  const [mode, setMode] = useState<Mode>("hybrid");
  const [profile, setProfile] = useState<CompanyProfile | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProfile().then(setProfile).catch(() => {});
  }, []);

  const handleUpload = async (file: File) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await uploadDocument(file, mode);
      setResult(res);
    } catch (e: any) {
      setError(e.message || "Wystąpił błąd");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async (p: CompanyProfile) => {
    const saved = await updateProfile(p);
    setProfile(saved);
  };

  return (
    <main className="max-w-3xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">TenderScope Document Filler</h1>
        <p className="text-gray-500 mt-1">
          Automatyczne uzupełnianie danych wykonawcy w dokumentach przetargowych
        </p>
      </div>

      <ModeToggle mode={mode} onChange={setMode} />

      {profile && <ProfileCard profile={profile} onSave={handleSaveProfile} />}

      <Upload onUpload={handleUpload} isLoading={loading} />

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
          {error}
        </div>
      )}

      {result && (
        <>
          <FieldPreview fields={result.fields} filename={result.filename} />
          <div className="flex gap-3">
            <a
              href={getDownloadUrl(result.document_id)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 inline-block"
            >
              Pobierz wypełniony dokument
            </a>
          </div>
        </>
      )}

      <footer className="text-xs text-gray-400 pt-8 border-t">
        Demo MVP — Dokodu × TenderScope | Tryb: {mode}
      </footer>
    </main>
  );
}
```

- [ ] **Step 8: Configure next.config.js for API proxy (dev)**

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      { source: "/api/:path*", destination: "http://localhost:8000/api/:path*" },
    ];
  },
};
module.exports = nextConfig;
```

- [ ] **Step 9: Test locally**

Terminal 1:
```bash
cd tender-doc-filler && uvicorn backend.main:app --reload --port 8000
```

Terminal 2:
```bash
cd tender-doc-filler/frontend && npm install && npm run dev
```

Open http://localhost:3000, upload a test DOCX, verify fields appear.

- [ ] **Step 10: Commit**

```bash
git add tender-doc-filler/frontend/
git commit -m "feat: Next.js frontend — upload, preview, profile, mode toggle"
```

---

## Task 7: Docker + Nginx + Deploy

**Files:**
- Create: `tender-doc-filler/Dockerfile`
- Create: `tender-doc-filler/nginx.conf`
- Create: `tender-doc-filler/README.md`

- [ ] **Step 1: Write Dockerfile (multi-stage)**

```dockerfile
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./backend/

# Copy frontend static build
COPY --from=frontend-build /app/frontend/out ./frontend-static/

# Copy nginx config
COPY nginx.conf /etc/nginx/sites-enabled/default

# Cleanup script
RUN echo '#!/bin/sh\nfind /tmp/tender -mindepth 1 -maxdepth 1 -mmin +60 -exec rm -rf {} +' > /usr/local/bin/cleanup.sh && chmod +x /usr/local/bin/cleanup.sh

EXPOSE 80

CMD sh -c "mkdir -p /tmp/tender && \
    (while true; do /usr/local/bin/cleanup.sh; sleep 300; done &) && \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
    nginx -g 'daemon off;'"
```

- [ ] **Step 2: Write nginx.conf**

```nginx
server {
    listen 80;
    server_name tender-demo.dokodu.it;

    root /app/frontend-static;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 20M;
        proxy_read_timeout 60s;
    }

    location / {
        try_files $uri $uri.html /index.html;
    }
}
```

- [ ] **Step 3: Update next.config.js for static export**

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  async rewrites() {
    return [
      { source: "/api/:path*", destination: "http://localhost:8000/api/:path*" },
    ];
  },
};
module.exports = nextConfig;
```

Note: `rewrites` only works in dev mode. In production, nginx handles proxying.

- [ ] **Step 4: Write README.md**

```markdown
# TenderScope Document Filler — MVP Demo

Automatyczne uzupełnianie danych wykonawcy w dokumentach przetargowych (DOCX).

## Quick Start (dev)

Backend:
    cd tender-doc-filler && pip install -r backend/requirements.txt
    uvicorn backend.main:app --reload --port 8000

Frontend:
    cd tender-doc-filler/frontend && npm install && npm run dev

## Docker

    docker build -t tender-filler .
    docker run -p 80:80 -e ANTHROPIC_API_KEY=sk-... tender-filler

## Tryby

- **Regułowy** — regex + table matching, szybki, 100% pewny na znanych polach
- **AI** — Claude Sonnet rozpoznaje pola z treści dokumentu
- **Hybrydowy** — reguły first, AI fallback dla nieznalezionych pól
```

- [ ] **Step 5: Build and test Docker locally**

```bash
cd tender-doc-filler && docker build -t tender-filler .
docker run -p 8080:80 -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-dummy} tender-filler
```

Open http://localhost:8080, test upload flow.

- [ ] **Step 6: Deploy to server**

```bash
# Confirm with Kacper before pushing
ssh deploy@57.128.219.9 "mkdir -p ~/tender-demo"
scp -r tender-doc-filler/* deploy@57.128.219.9:~/tender-demo/
ssh deploy@57.128.219.9 "cd ~/tender-demo && docker build -t tender-filler . && docker run -d --name tender-demo -p 8090:80 --restart unless-stopped -e ANTHROPIC_API_KEY=\$ANTHROPIC_API_KEY tender-filler"
```

Then configure nginx on server to proxy `tender-demo.dokodu.it` to port 8090.

- [ ] **Step 7: Commit**

```bash
git add tender-doc-filler/Dockerfile tender-doc-filler/nginx.conf tender-doc-filler/README.md
git commit -m "feat: Docker + nginx config for deployment"
```

---

## Task 8: End-to-End Validation on Real Documents

- [ ] **Step 1: Test all 7 TenderScope documents via the running app**

Upload each of the 7 DOCX files in rule mode, verify field counts match POC (24 total in 5 docs).

- [ ] **Step 2: Test hybrid mode on the 2 problematic documents**

Upload `Zał.3.a_Formularz_ofertowy_cz1.docx` and `Załącznik nr 4 - oswiadczenie...docx` in hybrid mode. Verify AI picks up the paragraph-based fields.

- [ ] **Step 3: Download filled documents and verify in Word/LibreOffice**

Open each `FILLED_*.docx` — check values are correct and formatting is preserved.

- [ ] **Step 4: Fix any issues found**

- [ ] **Step 5: Final commit**

```bash
git add -A && git commit -m "test: validate on real TenderScope documents"
```
