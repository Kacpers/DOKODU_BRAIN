"""Tests for brain_parser.py — DOKODU BRAIN markdown parser."""

import pytest
from brain_parser import (
    append_meeting_section,
    extract_sync_section,
    parse_meeting_sections,
    parse_outreach_table,
    parse_pipeline_table,
    parse_profile_yaml,
    parse_reminders,
    update_profile_yaml,
    update_sync_section,
)


# ---------------------------------------------------------------------------
# extract_sync_section / update_sync_section
# ---------------------------------------------------------------------------

CONTENT_WITH_SYNC = """\
# CRM — LEADY B2B

## PIPELINE AKTYWNY

<!-- SYNC:PIPELINE -->
| # | Firma | Kontakt | Etap |
| :- | :--- | :--- | :--- |
| 1 | Animex | Kamil | WYGRANA |
<!-- /SYNC:PIPELINE -->

## Other section

Some other content here.
"""


class TestExtractSyncSection:
    def test_extracts_content_between_markers(self):
        result = extract_sync_section(CONTENT_WITH_SYNC, "PIPELINE")
        assert "Animex" in result
        assert "<!-- SYNC:" not in result
        assert "<!-- /SYNC:" not in result

    def test_returns_empty_string_when_marker_missing(self):
        result = extract_sync_section(CONTENT_WITH_SYNC, "NONEXISTENT")
        assert result == ""

    def test_returns_empty_string_on_empty_content(self):
        assert extract_sync_section("", "PIPELINE") == ""

    def test_preserves_whitespace_inside_section(self):
        result = extract_sync_section(CONTENT_WITH_SYNC, "PIPELINE")
        assert result.startswith("\n")

    def test_multiline_content(self):
        content = "<!-- SYNC:TEST -->\nline1\nline2\nline3\n<!-- /SYNC:TEST -->"
        result = extract_sync_section(content, "TEST")
        assert "line1" in result
        assert "line2" in result
        assert "line3" in result


class TestUpdateSyncSection:
    def test_replaces_section_content(self):
        new = "\n| # | Firma |\n| 1 | NewCo |\n"
        result = update_sync_section(CONTENT_WITH_SYNC, "PIPELINE", new)
        assert "NewCo" in result
        assert "Animex" not in result

    def test_preserves_content_outside_markers(self):
        new = "\nnew content\n"
        result = update_sync_section(CONTENT_WITH_SYNC, "PIPELINE", new)
        assert "## Other section" in result
        assert "Some other content here." in result
        assert "## PIPELINE AKTYWNY" in result

    def test_preserves_markers_themselves(self):
        new = "\nnew\n"
        result = update_sync_section(CONTENT_WITH_SYNC, "PIPELINE", new)
        assert "<!-- SYNC:PIPELINE -->" in result
        assert "<!-- /SYNC:PIPELINE -->" in result

    def test_returns_unchanged_when_marker_not_found(self):
        result = update_sync_section(CONTENT_WITH_SYNC, "MISSING", "x")
        assert result == CONTENT_WITH_SYNC

    def test_roundtrip_with_extract(self):
        original = extract_sync_section(CONTENT_WITH_SYNC, "PIPELINE")
        result = update_sync_section(CONTENT_WITH_SYNC, "PIPELINE", original)
        assert result == CONTENT_WITH_SYNC


# ---------------------------------------------------------------------------
# parse_pipeline_table
# ---------------------------------------------------------------------------

PIPELINE_SECTION = """
| # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline |
| :- | :--- | :--- | :--- | :--- | ---: | :--- | :---: |
| 1 | Animex | Kamil Kowalski | Ref. | WYGRANA | 18 000 | Faktura za szkolenia | 2026-04-07 |
| 2 | Corleonis | [imie] | LinkedIn | WYGRANA | 35 000 | Faza UAT | — |
| 3 | TenderScope | Borys Kowalik | Inbound (dokodu.it) | Kontakt | ~20 000 | Czekamy na odpowiedzi | 2026-04-03 |
| 4 | Adm. Gibula | Jakub Gibula | Istniejący klient | Discovery | ~55 000 | Call sobota 04.04 | 2026-04-04 |
| 5 | ___ | ___ | ___ | Nowy | ___ | Kwalifikacja | ___ |
"""


class TestParsePipelineTable:
    def test_returns_correct_number_of_rows(self):
        rows = parse_pipeline_table(PIPELINE_SECTION)
        assert len(rows) == 4  # placeholder row skipped

    def test_first_row_fields(self):
        rows = parse_pipeline_table(PIPELINE_SECTION)
        r = rows[0]
        assert r["nr"] == "1"
        assert r["firma"] == "Animex"
        assert r["kontakt"] == "Kamil Kowalski"
        assert r["etap"] == "WYGRANA"
        assert r["wartosc"] == "18 000"
        assert r["deadline"] == "2026-04-07"

    def test_tilde_wartosc_preserved(self):
        rows = parse_pipeline_table(PIPELINE_SECTION)
        tender = next(r for r in rows if r["firma"] == "TenderScope")
        assert tender["wartosc"] == "~20 000"

    def test_placeholder_row_skipped(self):
        rows = parse_pipeline_table(PIPELINE_SECTION)
        firmy = [r["firma"] for r in rows]
        assert "___" not in firmy

    def test_empty_section(self):
        rows = parse_pipeline_table("")
        assert rows == []

    def test_header_only_section(self):
        section = "| # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline |\n| :- | :--- | :--- | :--- | :--- | ---: | :--- | :---: |"
        rows = parse_pipeline_table(section)
        assert rows == []

    def test_all_keys_present(self):
        rows = parse_pipeline_table(PIPELINE_SECTION)
        expected_keys = {"nr", "firma", "kontakt", "zrodlo", "etap", "wartosc", "nastepny_krok", "deadline"}
        for row in rows:
            assert set(row.keys()) == expected_keys


# ---------------------------------------------------------------------------
# parse_outreach_table
# ---------------------------------------------------------------------------

OUTREACH_SECTION = """
| # | Firma | Osoba | Stanowisko | Score | Data zaproszenia | Status | Następny krok | Follow-up |
|---|-------|-------|-----------|-------|-----------------|--------|---------------|-----------|
| 1 | VTS Group | Rafał Wiatr | CTO | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
| 2a | Rossmann SDP | Małgorzata Kołodziejczyk | IT Director | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
| 2b | Rossmann SDP | Piotr Jugiel | IT Director | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
| 2c | Rossmann SDP | Anna Hesiak | Analityk Procesów | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
| 3 | CAPITAL SERVICE S.A. | Marzena Szulim | Head of Risk | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
| 4a | UNIQA Polska | Błażej Misztal | Lider Zespołu Gen AI | A | 2026-03-30 | dm_wysłany | Czekaj na odpowiedź | 2026-04-02 |
| 5b | Media Expert / TERG | Przemysław Płaczek | Manager ds. raportowania | A | 2026-03-30 | dm_wysłany | Czekaj na odpowiedź | 2026-04-03 |
| 5b-note | ↳ Płaczek poinformowany 01.04 | | | | | | | |
| 5c | Media Expert / TERG | Anna Frąckiel | Kierownik ds. Szkoleń | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
"""


class TestParseOutreachTable:
    def test_note_rows_skipped(self):
        rows = parse_outreach_table(OUTREACH_SECTION)
        nrs = [r["nr"] for r in rows]
        assert "5b-note" not in nrs

    def test_continuation_rows_skipped(self):
        rows = parse_outreach_table(OUTREACH_SECTION)
        firmy = [r["firma"] for r in rows]
        for firma in firmy:
            assert not firma.startswith("↳")

    def test_multi_row_company_counted_separately(self):
        rows = parse_outreach_table(OUTREACH_SECTION)
        rossmann = [r for r in rows if r["firma"] == "Rossmann SDP"]
        assert len(rossmann) == 3  # 2a, 2b, 2c

    def test_nr_format_preserved(self):
        rows = parse_outreach_table(OUTREACH_SECTION)
        nrs = [r["nr"] for r in rows]
        assert "2a" in nrs
        assert "2b" in nrs
        assert "2c" in nrs

    def test_total_row_count(self):
        rows = parse_outreach_table(OUTREACH_SECTION)
        # 1, 2a, 2b, 2c, 3, 4a, 5b, 5c = 8 rows (5b-note skipped)
        assert len(rows) == 8

    def test_empty_section(self):
        rows = parse_outreach_table("")
        assert rows == []

    def test_all_keys_present(self):
        rows = parse_outreach_table(OUTREACH_SECTION)
        expected_keys = {"nr", "firma", "osoba", "stanowisko", "score", "data_zaproszenia", "status", "nastepny_krok", "follow_up"}
        for row in rows:
            assert set(row.keys()) == expected_keys

    def test_second_table_block_without_separator(self):
        """Outreach_Tracker has a blank line then a second block of rows in the same table.
        Both blocks should be parsed correctly."""
        section = """
| # | Firma | Osoba | Stanowisko | Score | Data zaproszenia | Status | Następny krok | Follow-up |
|---|-------|-------|-----------|-------|-----------------|--------|---------------|-----------|
| 1 | Alpha | Jan Kowalski | CEO | A | 2026-04-01 | zaproszenie_wysłane | DM | 2026-04-05 |

| 2 | Beta | Maria Nowak | CTO | A | 2026-04-01 | zaproszenie_wysłane | DM | 2026-04-05 |
"""
        rows = parse_outreach_table(section)
        firmy = [r["firma"] for r in rows]
        assert "Alpha" in firmy
        assert "Beta" in firmy


# ---------------------------------------------------------------------------
# parse_profile_yaml / update_profile_yaml
# ---------------------------------------------------------------------------

PROFILE_CONTENT = """\
---
type: prospect
status: discovery
owner: kacper
created: 2026-03-30
wartosc_est: 62 000–66 000 PLN netto
tags: [prospect, holandia, faktury]
---

# Administratiekantoor Gibula

## Dane kontaktowe
- Kontakt: Jakub Gibula
"""


class TestParseProfileYaml:
    def test_extracts_all_fields(self):
        data = parse_profile_yaml(PROFILE_CONTENT)
        assert data["type"] == "prospect"
        assert data["status"] == "discovery"
        assert data["owner"] == "kacper"

    def test_extracts_list_field(self):
        data = parse_profile_yaml(PROFILE_CONTENT)
        assert isinstance(data["tags"], list)
        assert "faktury" in data["tags"]

    def test_missing_frontmatter_returns_empty_dict(self):
        content = "# Just a title\n\nSome content."
        data = parse_profile_yaml(content)
        assert data == {}

    def test_empty_content_returns_empty_dict(self):
        assert parse_profile_yaml("") == {}

    def test_frontmatter_only_file(self):
        content = "---\ntype: area\n---\n"
        data = parse_profile_yaml(content)
        assert data["type"] == "area"


class TestUpdateProfileYaml:
    def test_updates_existing_field(self):
        updated = update_profile_yaml(PROFILE_CONTENT, {"status": "propozycja"})
        data = parse_profile_yaml(updated)
        assert data["status"] == "propozycja"

    def test_adds_new_field(self):
        updated = update_profile_yaml(PROFILE_CONTENT, {"crm_id": "CRM-042"})
        data = parse_profile_yaml(updated)
        assert data["crm_id"] == "CRM-042"

    def test_preserves_other_fields(self):
        updated = update_profile_yaml(PROFILE_CONTENT, {"status": "wygrana"})
        data = parse_profile_yaml(updated)
        assert data["type"] == "prospect"
        assert data["owner"] == "kacper"

    def test_preserves_body_after_frontmatter(self):
        updated = update_profile_yaml(PROFILE_CONTENT, {"status": "wygrana"})
        assert "## Dane kontaktowe" in updated
        assert "Jakub Gibula" in updated

    def test_no_frontmatter_returns_unchanged(self):
        content = "# No frontmatter\n\nContent here."
        result = update_profile_yaml(content, {"status": "new"})
        assert result == content

    def test_multiple_updates_at_once(self):
        updated = update_profile_yaml(PROFILE_CONTENT, {"status": "wygrana", "owner": "alina"})
        data = parse_profile_yaml(updated)
        assert data["status"] == "wygrana"
        assert data["owner"] == "alina"


# ---------------------------------------------------------------------------
# parse_meeting_sections / append_meeting_section
# ---------------------------------------------------------------------------

MEETINGS_CONTENT = """\
---
type: meeting-log
status: active
owner: kacper
---

# SPOTKANIA: Animex
> Log spotkań.

---

## 2026-03-28 — Rozmowa podsumowująca projekt

Omówiono zamknięcie projektu.

Ustalono wystawienie faktury końcowej.

## 2026-02-15 — Kick-off szkolenia

Omówiono cele szkolenia.
Plan na 3 grupy.

## 2026-01-10 — Wstępny call

Pierwszy kontakt po rekomendacji.
"""


class TestParseMeetingSections:
    def test_returns_three_sections(self):
        sections = parse_meeting_sections(MEETINGS_CONTENT)
        assert len(sections) == 3

    def test_sorted_newest_first(self):
        sections = parse_meeting_sections(MEETINGS_CONTENT)
        dates = [s["date"] for s in sections]
        assert dates == sorted(dates, reverse=True)

    def test_first_section_is_newest(self):
        sections = parse_meeting_sections(MEETINGS_CONTENT)
        assert sections[0]["date"] == "2026-03-28"

    def test_last_section_is_oldest(self):
        sections = parse_meeting_sections(MEETINGS_CONTENT)
        assert sections[-1]["date"] == "2026-01-10"

    def test_title_extracted_correctly(self):
        sections = parse_meeting_sections(MEETINGS_CONTENT)
        titles = {s["date"]: s["title"] for s in sections}
        assert titles["2026-03-28"] == "Rozmowa podsumowująca projekt"
        assert titles["2026-02-15"] == "Kick-off szkolenia"

    def test_content_extracted(self):
        sections = parse_meeting_sections(MEETINGS_CONTENT)
        newest = next(s for s in sections if s["date"] == "2026-03-28")
        assert "zamknięcie projektu" in newest["content"]
        assert "faktury końcowej" in newest["content"]

    def test_empty_content_returns_empty_list(self):
        assert parse_meeting_sections("") == []

    def test_no_meeting_sections_returns_empty_list(self):
        content = "# Title\n\nJust some content.\n"
        assert parse_meeting_sections(content) == []


class TestAppendMeetingSection:
    def test_new_section_appears_in_output(self):
        result = append_meeting_section(
            MEETINGS_CONTENT,
            "2026-04-01",
            "Nowy call",
            "Ustalono kolejny krok.",
        )
        assert "2026-04-01 — Nowy call" in result

    def test_new_section_before_existing_sections(self):
        result = append_meeting_section(
            MEETINGS_CONTENT,
            "2026-04-01",
            "Nowy call",
            "Ustalono kolejny krok.",
        )
        pos_new = result.find("2026-04-01")
        pos_old = result.find("2026-03-28")
        assert pos_new < pos_old

    def test_old_sections_preserved(self):
        result = append_meeting_section(
            MEETINGS_CONTENT,
            "2026-04-01",
            "Nowy call",
            "Body.",
        )
        assert "Rozmowa podsumowująca projekt" in result
        assert "Kick-off szkolenia" in result
        assert "Wstępny call" in result

    def test_parse_after_append_gives_sorted_order(self):
        result = append_meeting_section(
            MEETINGS_CONTENT,
            "2026-04-01",
            "Nowy call",
            "Body.",
        )
        sections = parse_meeting_sections(result)
        assert len(sections) == 4
        assert sections[0]["date"] == "2026-04-01"

    def test_append_to_empty_meetings(self):
        content = "# SPOTKANIA: Test\n\n---\n\n"
        result = append_meeting_section(content, "2026-04-01", "Pierwszy call", "Treść.")
        assert "2026-04-01 — Pierwszy call" in result

    def test_body_included_in_section(self):
        result = append_meeting_section(
            MEETINGS_CONTENT,
            "2026-04-01",
            "Nowy call",
            "Szczegółowe ustalenia: X, Y, Z.",
        )
        assert "Szczegółowe ustalenia: X, Y, Z." in result


# ---------------------------------------------------------------------------
# parse_reminders
# ---------------------------------------------------------------------------

REMINDERS_CONTENT = """\
---
type: reminders
---

# Reminders

## Aktywne

- 2026-03-27 | SEO | Sprawdź CTR frazy "llm" po zmianie title/meta
- 2026-04-03 | SEO | Czy /blog/n8n awansował po poprawie internal linkingu
- 2026-04-02 | INNE | Fryzjer 15:30 + nagranie VSL kursu n8n
- 2026-04-04 | BIZNES | 9:30 Call z Jakubem Gibulą — Gibula
- ~~2026-03-27 | BIZNES | Animex: napisz do Kamila Kowalskiego~~ → DONE
- 2026-04-07 | BIZNES | Animex: follow-up do Kamila ws. wdrożenia n8n
- 2026-04-01 | BIZNES | Animex: wystawić fakturę za szkolenia

## Wykonane

"""


class TestParseReminders:
    def test_returns_correct_count(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        # 6 active + 1 strikethrough (skipped) = 6
        assert len(reminders) == 6

    def test_completed_reminder_skipped(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        texts = [r["text"] for r in reminders]
        assert not any("napisz do Kamila Kowalskiego" in t for t in texts)

    def test_date_extracted(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        dates = [r["date"] for r in reminders]
        assert "2026-04-04" in dates

    def test_category_extracted(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        gibula = next(r for r in reminders if "Gibula" in r["text"])
        assert gibula["category"] == "BIZNES"

    def test_text_extracted(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        seo = next(r for r in reminders if "llm" in r["text"])
        assert "CTR frazy" in seo["text"]

    def test_all_keys_present(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        for r in reminders:
            assert set(r.keys()) == {"date", "category", "text"}

    def test_empty_content(self):
        assert parse_reminders("") == []

    def test_no_reminders(self):
        content = "# Reminders\n\nNo entries yet.\n"
        assert parse_reminders(content) == []

    def test_mixed_categories(self):
        reminders = parse_reminders(REMINDERS_CONTENT)
        categories = {r["category"] for r in reminders}
        assert "SEO" in categories
        assert "BIZNES" in categories
        assert "INNE" in categories
