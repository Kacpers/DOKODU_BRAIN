#!/usr/bin/env python3
"""
DOKODU BRAIN — YouTube Ideas Bank
Zarządza bankiem pomysłów na odcinki YouTube w lokalnej bazie SQLite.

Użycie:
  python3 youtube_ideas.py add "Tytuł pomysłu" --pillar "Tutorial n8n" --notes "..."
  python3 youtube_ideas.py list
  python3 youtube_ideas.py list --status POMYSŁ --priority high
  python3 youtube_ideas.py update 3 --status SCENARIUSZ --priority high
  python3 youtube_ideas.py show 3
  python3 youtube_ideas.py delete 3
"""

import sys
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

DB_FILE = Path.home() / ".config" / "dokodu" / "yt_data.db"

STATUSES   = ["POMYSŁ", "SCENARIUSZ", "NAGRANIE", "MONTAŻ", "GOTOWY", "OPUBLIKOWANY", "POMINIĘTY"]
PRIORITIES = ["high", "medium", "low"]
PILLARS    = ["Tutorial n8n", "Local AI", "Case study", "AI Act / RODO", "Automatyzacja B2B", "Behind scenes", "Inne"]
VERDICTS   = {"green": "🟢", "yellow": "🟡", "red": "🔴", "🟢": "🟢", "🟡": "🟡", "🔴": "🔴"}
SOURCES    = ["manual", "yt-research", "yt-competitive", "yt-plan-video", "inbox"]


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_FILE)
    c.row_factory = sqlite3.Row
    return c


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ═══════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════

def cmd_add(args):
    db = conn()
    verdict = VERDICTS.get(args.verdict, "🟡")
    db.execute("""
        INSERT INTO video_ideas (title, topic, pillar, angle, status, priority, verdict, source, research_file, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (args.title, args.topic, args.pillar, args.angle,
          args.status, args.priority, verdict, args.source,
          args.research_file, args.notes))
    db.commit()
    idea_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    print(f"✅ Dodano pomysł #{idea_id}: \"{args.title}\"")


def cmd_list(args):
    db = conn()
    query = "SELECT * FROM video_ideas WHERE 1=1"
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

    print(f"\n{'ID':>3}  {'V':2}  {'Pri':6}  {'Status':12}  {'Pillar':20}  Tytuł")
    print("─" * 90)
    for r in rows:
        pillar = (r["pillar"] or "—")[:20]
        title  = (r["title"] or "")[:45]
        pri    = {"high": "🔴 high", "medium": "🟡 med", "low": "⚪ low"}.get(r["priority"], r["priority"])
        print(f"{r['id']:>3}  {r['verdict']:2}  {pri:6}  {r['status']:12}  {pillar:20}  {title}")

    print(f"\nŁącznie: {len(rows)} pomysłów")


def cmd_show(args):
    db = conn()
    r = db.execute("SELECT * FROM video_ideas WHERE id = ?", (args.id,)).fetchone()
    db.close()

    if not r:
        print(f"Nie znaleziono pomysłu #{args.id}")
        return

    print(f"""
┌─────────────────────────────────────────────────────────
│ #{r['id']} — {r['title']}
├─────────────────────────────────────────────────────────
│ Verdict:   {r['verdict']}   Status: {r['status']}   Priorytet: {r['priority']}
│ Pillar:    {r['pillar'] or '—'}
│ Kąt:       {r['angle'] or '—'}
│ Temat:     {r['topic'] or '—'}
│ Źródło:    {r['source'] or '—'}
│ Research:  {r['research_file'] or '—'}
│ YT ID:     {r['yt_video_id'] or '—'}
│ Dodano:    {r['created_at']}
│ Aktualizacja: {r['updated_at']}
├─────────────────────────────────────────────────────────
│ Notatki:
│ {(r['notes'] or '—').replace(chr(10), chr(10) + '│ ')}
└─────────────────────────────────────────────────────────""")


def cmd_update(args):
    db = conn()
    r = db.execute("SELECT * FROM video_ideas WHERE id = ?", (args.id,)).fetchone()
    if not r:
        print(f"Nie znaleziono pomysłu #{args.id}")
        db.close()
        return

    fields = {"updated_at": now()}
    if args.status:   fields["status"]   = args.status
    if args.priority: fields["priority"] = args.priority
    if args.verdict:  fields["verdict"]  = VERDICTS.get(args.verdict, args.verdict)
    if args.pillar:   fields["pillar"]   = args.pillar
    if args.angle:    fields["angle"]    = args.angle
    if args.notes:    fields["notes"]    = args.notes
    if args.yt_id:    fields["yt_video_id"] = args.yt_id

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE video_ideas SET {set_clause} WHERE id = ?",
               list(fields.values()) + [args.id])
    db.commit()
    db.close()
    print(f"✅ Zaktualizowano #{args.id}: {', '.join(f'{k}={v}' for k, v in fields.items() if k != 'updated_at')}")


def cmd_delete(args):
    db = conn()
    r = db.execute("SELECT title FROM video_ideas WHERE id = ?", (args.id,)).fetchone()
    if not r:
        print(f"Nie znaleziono pomysłu #{args.id}")
        db.close()
        return
    confirm = input(f"Usunąć #{args.id} \"{r['title']}\"? [t/N]: ")
    if confirm.lower() == "t":
        db.execute("DELETE FROM video_ideas WHERE id = ?", (args.id,))
        db.commit()
        print(f"✅ Usunięto #{args.id}")
    db.close()


def cmd_export(args):
    """Eksportuje pomysły do Markdown."""
    db = conn()
    rows = db.execute("""
        SELECT * FROM video_ideas
        WHERE status NOT IN ('POMINIĘTY')
        ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                 CASE verdict WHEN '🟢' THEN 1 WHEN '🟡' THEN 2 ELSE 3 END,
                 created_at DESC
    """).fetchall()
    db.close()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Bank Pomysłów YouTube",
        f"Eksport: {now_str} | Łącznie: {len(rows)} pomysłów\n",
        "| ID | V | Priorytet | Status | Pillar | Tytuł | Notatki |",
        "|----|---|-----------|--------|--------|-------|---------|",
    ]
    for r in rows:
        notes = (r["notes"] or "").replace("\n", " ")[:60]
        lines.append(
            f"| {r['id']} | {r['verdict']} | {r['priority']} | {r['status']} | "
            f"{r['pillar'] or '—'} | {r['title']} | {notes} |"
        )

    md = "\n".join(lines)
    print(md)

    if args.save:
        out = Path(__file__).parent.parent / "20_AREAS" / "AREA_YouTube" / "YT_Ideas_Bank.md"
        out.write_text(md, encoding="utf-8")
        print(f"\n✅ Zapisano: {out}", file=sys.stderr)


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="YouTube Ideas Bank")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ADD
    p_add = sub.add_parser("add", help="Dodaj pomysł")
    p_add.add_argument("title")
    p_add.add_argument("--topic",         default=None)
    p_add.add_argument("--pillar",        default=None, choices=PILLARS)
    p_add.add_argument("--angle",         default=None)
    p_add.add_argument("--status",        default="POMYSŁ", choices=STATUSES)
    p_add.add_argument("--priority",      default="medium", choices=PRIORITIES)
    p_add.add_argument("--verdict",       default="🟡")
    p_add.add_argument("--source",        default="manual", choices=SOURCES)
    p_add.add_argument("--research-file", default=None, dest="research_file")
    p_add.add_argument("--notes",         default=None)

    # LIST
    p_list = sub.add_parser("list", help="Lista pomysłów")
    p_list.add_argument("--status",   default=None)
    p_list.add_argument("--priority", default=None)
    p_list.add_argument("--pillar",   default=None)
    p_list.add_argument("--verdict",  default=None)
    p_list.add_argument("--all",      action="store_true", help="Pokaż też opublikowane/pominięte")

    # SHOW
    p_show = sub.add_parser("show", help="Szczegóły pomysłu")
    p_show.add_argument("id", type=int)

    # UPDATE
    p_upd = sub.add_parser("update", help="Aktualizuj pomysł")
    p_upd.add_argument("id", type=int)
    p_upd.add_argument("--status",   default=None, choices=STATUSES)
    p_upd.add_argument("--priority", default=None, choices=PRIORITIES)
    p_upd.add_argument("--verdict",  default=None)
    p_upd.add_argument("--pillar",   default=None)
    p_upd.add_argument("--angle",    default=None)
    p_upd.add_argument("--notes",    default=None)
    p_upd.add_argument("--yt-id",    default=None, dest="yt_id")

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
