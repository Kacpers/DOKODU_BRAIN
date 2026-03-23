#!/usr/bin/env python3
"""
DOKODU BRAIN — Blog SEO Ideas Bank
Zarządza bankiem pomysłów na posty blogowe w lokalnej bazie SQLite.

Użycie:
  python3 seo_ideas.py add "Tytuł posta" --keyword "microsoft 365 copilot wdrożenie" --pillar "M365 Copilot"
  python3 seo_ideas.py list
  python3 seo_ideas.py list --status POMYSŁ --priority high
  python3 seo_ideas.py update 3 --status BRIEF --priority high
  python3 seo_ideas.py show 3
  python3 seo_ideas.py delete 3
  python3 seo_ideas.py export --save
"""

import sys
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

DB_FILE = Path.home() / ".config" / "dokodu" / "gsc_data.db"

STATUSES = [
    "POMYSŁ",       # surowy pomysł
    "KEYWORD",      # przypisane słowo kluczowe, zbadany intent
    "BRIEF",        # gotowy brief z H2/H3 i meta
    "PISANIE",      # w trakcie pisania
    "REVIEW",       # gotowy, wymaga review
    "OPUBLIKOWANY", # live na blogu
    "POMINIĘTY",    # odrzucony
]
PRIORITIES = ["high", "medium", "low"]
PILLARS    = [
    "M365 Copilot",
    "GitHub Copilot",
    "n8n Automatyzacja",
    "AI w firmie",
    "AI Act / Compliance",
    "Docker / Dev Tools",
    "Inne",
]
INTENTS = ["informational", "commercial", "navigational", "transactional"]
VERDICTS = {"green": "🟢", "yellow": "🟡", "red": "🔴", "🟢": "🟢", "🟡": "🟡", "🔴": "🔴"}
SOURCES  = ["manual", "gsc-sync", "seo-research", "seo-plan-post", "inbox", "competitor"]


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_FILE)
    c.row_factory = sqlite3.Row
    return c


def ensure_table():
    db = conn()
    db.execute("""
        CREATE TABLE IF NOT EXISTS blog_ideas (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            title              TEXT NOT NULL,
            target_keyword     TEXT,
            secondary_keywords TEXT,
            search_intent      TEXT DEFAULT 'informational',
            pillar             TEXT,
            status             TEXT DEFAULT 'POMYSŁ',
            priority           TEXT DEFAULT 'medium',
            verdict            TEXT DEFAULT '🟡',
            source             TEXT DEFAULT 'manual',
            related_page       TEXT,
            target_position    INTEGER,
            current_position   REAL,
            monthly_volume     INTEGER,
            notes              TEXT,
            slug               TEXT,
            meta_title         TEXT,
            meta_description   TEXT,
            created_at         TEXT DEFAULT (datetime('now')),
            updated_at         TEXT DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ═══════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════

def cmd_add(args):
    ensure_table()
    db = conn()
    verdict = VERDICTS.get(args.verdict, "🟡")
    db.execute("""
        INSERT INTO blog_ideas
        (title, target_keyword, secondary_keywords, search_intent, pillar,
         status, priority, verdict, source, related_page, target_position,
         monthly_volume, notes, slug)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        args.title,
        args.keyword,
        args.secondary,
        args.intent,
        args.pillar,
        args.status,
        args.priority,
        verdict,
        args.source,
        args.related_page,
        args.target_position,
        args.volume,
        args.notes,
        args.slug,
    ))
    db.commit()
    idea_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    print(f"✅ Dodano pomysł #{idea_id}: \"{args.title}\"")


def cmd_list(args):
    ensure_table()
    db = conn()
    query  = "SELECT * FROM blog_ideas WHERE 1=1"
    params = []

    if args.status:
        query += " AND status = ?"
        params.append(args.status)
    if args.priority:
        query += " AND priority = ?"
        params.append(args.priority)
    if args.pillar:
        query += " AND pillar LIKE ?"
        params.append(f"%{args.pillar}%")
    if args.verdict:
        query += " AND verdict = ?"
        params.append(VERDICTS.get(args.verdict, args.verdict))
    if not args.all:
        query += " AND status NOT IN ('OPUBLIKOWANY', 'POMINIĘTY')"

    query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, created_at DESC"

    rows = db.execute(query, params).fetchall()
    db.close()

    if not rows:
        print("Brak pomysłów spełniających kryteria.")
        return

    print(f"\n{'ID':>3}  {'V':2}  {'Pri':6}  {'Status':12}  {'Pillar':18}  {'Keyword':25}  Tytuł")
    print("─" * 110)
    for r in rows:
        pillar  = (r["pillar"] or "—")[:18]
        keyword = (r["target_keyword"] or "—")[:25]
        title   = (r["title"] or "")[:40]
        pri     = {"high": "🔴 high", "medium": "🟡 med", "low": "⚪ low"}.get(r["priority"], r["priority"])
        print(f"{r['id']:>3}  {r['verdict']:2}  {pri:6}  {r['status']:12}  {pillar:18}  {keyword:25}  {title}")

    print(f"\nŁącznie: {len(rows)} pomysłów")


def cmd_show(args):
    ensure_table()
    db = conn()
    r = db.execute("SELECT * FROM blog_ideas WHERE id = ?", (args.id,)).fetchone()
    db.close()
    if not r:
        print(f"Nie znaleziono pomysłu #{args.id}")
        return

    print(f"""
┌─────────────────────────────────────────────────────────
│ #{r['id']} — {r['title']}
├─────────────────────────────────────────────────────────
│ Verdict:    {r['verdict']}   Status: {r['status']}   Priorytet: {r['priority']}
│ Pillar:     {r['pillar'] or '—'}
│ Keyword:    {r['target_keyword'] or '—'}
│ Secondary:  {r['secondary_keywords'] or '—'}
│ Intent:     {r['search_intent'] or '—'}
│ Volume:     {r['monthly_volume'] or '—'} / mies.
│ Pozycja:    aktualna: {r['current_position'] or '—'}  |  cel: top {r['target_position'] or '—'}
│ Slug:       {r['slug'] or '—'}
│ Related:    {r['related_page'] or '—'}
│ Źródło:     {r['source'] or '—'}
│ Dodano:     {r['created_at']}
│ Update:     {r['updated_at']}
├─────────────────────────────────────────────────────────
│ Meta Title: {r['meta_title'] or '—'}
│ Meta Desc:  {r['meta_description'] or '—'}
├─────────────────────────────────────────────────────────
│ Notatki:
│ {(r['notes'] or '—').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────────""")


def cmd_update(args):
    ensure_table()
    db = conn()
    r = db.execute("SELECT * FROM blog_ideas WHERE id = ?", (args.id,)).fetchone()
    if not r:
        print(f"Nie znaleziono pomysłu #{args.id}")
        db.close()
        return

    fields = {"updated_at": now()}
    if args.status:           fields["status"]            = args.status
    if args.priority:         fields["priority"]          = args.priority
    if args.verdict:          fields["verdict"]           = VERDICTS.get(args.verdict, args.verdict)
    if args.pillar:           fields["pillar"]            = args.pillar
    if args.keyword:          fields["target_keyword"]    = args.keyword
    if args.notes:            fields["notes"]             = args.notes
    if args.slug:             fields["slug"]              = args.slug
    if args.meta_title:       fields["meta_title"]        = args.meta_title
    if args.meta_description: fields["meta_description"]  = args.meta_description
    if args.position:         fields["current_position"]  = args.position
    if args.volume:           fields["monthly_volume"]    = args.volume

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE blog_ideas SET {set_clause} WHERE id = ?",
               list(fields.values()) + [args.id])
    db.commit()
    db.close()
    print(f"✅ Zaktualizowano #{args.id}: {', '.join(f'{k}={v}' for k, v in fields.items() if k != 'updated_at')}")


def cmd_delete(args):
    ensure_table()
    db = conn()
    r = db.execute("SELECT title FROM blog_ideas WHERE id = ?", (args.id,)).fetchone()
    if not r:
        print(f"Nie znaleziono pomysłu #{args.id}")
        db.close()
        return
    confirm = input(f"Usunąć #{args.id} \"{r['title']}\"? [t/N]: ")
    if confirm.lower() == "t":
        db.execute("DELETE FROM blog_ideas WHERE id = ?", (args.id,))
        db.commit()
        print(f"✅ Usunięto #{args.id}")
    db.close()


def cmd_export(args):
    ensure_table()
    db = conn()
    rows = db.execute("""
        SELECT * FROM blog_ideas
        WHERE status NOT IN ('POMINIĘTY')
        ORDER BY
            CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
            CASE verdict  WHEN '🟢' THEN 1 WHEN '🟡' THEN 2 ELSE 3 END,
            created_at DESC
    """).fetchall()
    db.close()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Blog SEO — Bank Pomysłów",
        f"Eksport: {now_str} | Łącznie: {len(rows)} pomysłów\n",
        "| ID | V | Pri | Status | Pillar | Keyword | Tytuł | Notatki |",
        "|----|---|-----|--------|--------|---------|-------|---------|",
    ]
    for r in rows:
        notes = (r["notes"] or "").replace("\n", " ")[:50]
        lines.append(
            f"| {r['id']} | {r['verdict']} | {r['priority']} | {r['status']} | "
            f"{r['pillar'] or '—'} | {r['target_keyword'] or '—'} | {r['title']} | {notes} |"
        )

    md = "\n".join(lines)
    print(md)

    if args.save:
        from pathlib import Path as P
        out = P(__file__).parent.parent / "20_AREAS" / "AREA_Blog_SEO" / "SEO_Ideas_Bank.md"
        out.write_text(md, encoding="utf-8")
        print(f"\n✅ Zapisano: {out}", file=sys.stderr)


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════

def main():
    ensure_table()
    parser = argparse.ArgumentParser(description="Blog SEO Ideas Bank")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ADD
    p_add = sub.add_parser("add", help="Dodaj pomysł na post")
    p_add.add_argument("title")
    p_add.add_argument("--keyword",          default=None, dest="keyword",          help="Główne słowo kluczowe")
    p_add.add_argument("--secondary",        default=None,                          help="Dodatkowe słowa kluczowe (csv)")
    p_add.add_argument("--intent",           default="informational", choices=INTENTS)
    p_add.add_argument("--pillar",           default=None, choices=PILLARS)
    p_add.add_argument("--status",           default="POMYSŁ", choices=STATUSES)
    p_add.add_argument("--priority",         default="medium", choices=PRIORITIES)
    p_add.add_argument("--verdict",          default="🟡")
    p_add.add_argument("--source",           default="manual", choices=SOURCES)
    p_add.add_argument("--related-page",     default=None, dest="related_page",     help="URL powiązanej strony w domenie")
    p_add.add_argument("--target-position",  default=None, dest="target_position",  type=int)
    p_add.add_argument("--volume",           default=None, type=int,                help="Szacowany wolumen/mies.")
    p_add.add_argument("--slug",             default=None)
    p_add.add_argument("--notes",            default=None)

    # LIST
    p_list = sub.add_parser("list", help="Lista pomysłów")
    p_list.add_argument("--status",   default=None)
    p_list.add_argument("--priority", default=None)
    p_list.add_argument("--pillar",   default=None)
    p_list.add_argument("--verdict",  default=None)
    p_list.add_argument("--all",      action="store_true")

    # SHOW
    p_show = sub.add_parser("show", help="Szczegóły pomysłu")
    p_show.add_argument("id", type=int)

    # UPDATE
    p_upd = sub.add_parser("update", help="Aktualizuj pomysł")
    p_upd.add_argument("id", type=int)
    p_upd.add_argument("--status",           default=None, choices=STATUSES)
    p_upd.add_argument("--priority",         default=None, choices=PRIORITIES)
    p_upd.add_argument("--verdict",          default=None)
    p_upd.add_argument("--pillar",           default=None)
    p_upd.add_argument("--keyword",          default=None)
    p_upd.add_argument("--notes",            default=None)
    p_upd.add_argument("--slug",             default=None)
    p_upd.add_argument("--meta-title",       default=None, dest="meta_title")
    p_upd.add_argument("--meta-description", default=None, dest="meta_description")
    p_upd.add_argument("--position",         default=None, type=float)
    p_upd.add_argument("--volume",           default=None, type=int)

    # DELETE
    p_del = sub.add_parser("delete", help="Usuń pomysł")
    p_del.add_argument("id", type=int)

    # EXPORT
    p_exp = sub.add_parser("export", help="Eksportuj do Markdown")
    p_exp.add_argument("--save", action="store_true")

    args = parser.parse_args()
    {"add": cmd_add, "list": cmd_list, "show": cmd_show,
     "update": cmd_update, "delete": cmd_delete, "export": cmd_export}[args.cmd](args)


if __name__ == "__main__":
    main()
