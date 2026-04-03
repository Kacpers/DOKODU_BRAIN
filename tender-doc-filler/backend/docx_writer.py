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
