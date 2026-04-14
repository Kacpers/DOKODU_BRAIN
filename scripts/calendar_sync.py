#!/usr/bin/env python3
"""
Calendar Sync — DOKODU BRAIN
Pobiera eventy z Google Calendar (oba konta) i tworzy nowe.

Konta:
  1. ksieradzinski@gmail.com — Prywatny, AI Hero, Dokodu akcje, Familijne, Dzieci
  2. kacper@dokodu.it — Dokodu (primary), Rezerwacje-Konsultacje

Użycie:
  python3 calendar_sync.py --pull                      # eventy na najbliższe 7 dni
  python3 calendar_sync.py --pull --days 14             # na 14 dni
  python3 calendar_sync.py --pull --save                # zapisz do Calendar_Last_Sync.md
  python3 calendar_sync.py --create "Spotkanie X" --date 2026-04-15 --time 13:15
  python3 calendar_sync.py --create "Call Y" --date 2026-04-15 --time 10:00 --duration 30 --calendar "AI Hero"
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

# --- Config ---

SYNC_OUTPUT = Path.home() / "DOKODU_BRAIN" / "20_AREAS" / "AREA_Calendar" / "Calendar_Last_Sync.md"
OAUTH_PATH = Path.home() / ".gmail-mcp" / "gcp-oauth.keys.json"

# --- Accounts & Calendars ---

ACCOUNTS = {
    "ksieradzinski@gmail.com": {
        "creds": Path.home() / ".gmail-mcp" / "credentials.json",
        "calendars": {
            "Prywatny": "ksieradzinski@gmail.com",
            "AI Hero": "k.sieradzinski@aihero.pl",
            "Dokodu akcje": "20a8cd86fd13303182c55b034bc9ae8194783399b96765caedfe827a45373914@group.calendar.google.com",
            "Familijne": "family07240530149553983419@group.calendar.google.com",
            "Dzieci": "2qc2lcd1f7uvqvir3j7tedf3ls@group.calendar.google.com",
        },
    },
    "kacper@dokodu.it": {
        "creds": Path.home() / ".config" / "dokodu" / "dokodu_calendar_credentials.json",
        "calendars": {
            "Dokodu": "primary",
        },
    },
}

# Flat map of all calendars for --create
ALL_CALENDARS = {}
CALENDAR_ACCOUNT = {}
for account, info in ACCOUNTS.items():
    for cal_name, cal_id in info["calendars"].items():
        ALL_CALENDARS[cal_name] = cal_id
        CALENDAR_ACCOUNT[cal_name] = account

DEFAULT_CALENDAR = "Dokodu akcje"

CAL_API = "https://www.googleapis.com/calendar/v3"


def refresh_token(creds_path):
    """Refresh OAuth2 access token for a given credentials file."""
    creds = json.loads(creds_path.read_text())
    oauth = json.loads(OAUTH_PATH.read_text())
    client_info = oauth.get("installed", oauth.get("web", {}))

    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_info["client_id"],
            "client_secret": client_info["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        },
    )
    resp.raise_for_status()
    new_token = resp.json()["access_token"]

    creds["access_token"] = new_token
    creds_path.write_text(json.dumps(creds))
    return new_token


def get_events(token, calendar_id, time_min, time_max):
    """Fetch events from a single calendar."""
    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": True,
        "orderBy": "startTime",
        "timeZone": "Europe/Warsaw",
        "maxResults": 100,
    }
    r = requests.get(
        f"{CAL_API}/calendars/{calendar_id}/events",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    if r.status_code == 404:
        return []
    r.raise_for_status()
    return r.json().get("items", [])


def create_event(token, calendar_id, summary, date_str, time_str, duration_min=60, description=""):
    """Create a calendar event."""
    start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(minutes=duration_min)

    event_body = {
        "summary": summary,
        "start": {
            "dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Europe/Warsaw",
        },
        "end": {
            "dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Europe/Warsaw",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 30},
                {"method": "popup", "minutes": 10},
            ],
        },
    }
    if description:
        event_body["description"] = description

    r = requests.post(
        f"{CAL_API}/calendars/{calendar_id}/events",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=event_body,
    )
    r.raise_for_status()
    return r.json()


def format_event(event, calendar_name):
    """Format a single event for display."""
    start = event.get("start", {})
    start_dt = start.get("dateTime", "")
    start_date = start.get("date", "")
    summary = event.get("summary", "(brak tytułu)")

    if start_dt:
        # Timed event
        dt = datetime.fromisoformat(start_dt)
        time_str = dt.strftime("%H:%M")
        date_str = dt.strftime("%Y-%m-%d")
        day_name = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Ndz"][dt.weekday()]
        return f"  {time_str} | {summary} [{calendar_name}]", date_str, day_name, dt
    elif start_date:
        # All-day event
        dt = datetime.strptime(start_date, "%Y-%m-%d")
        day_name = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Ndz"][dt.weekday()]
        return f"  cały dzień | {summary} [{calendar_name}]", start_date, day_name, dt
    return None, None, None, None


def pull_events(tokens, days):
    """Pull events from all accounts and calendars, return grouped by date."""
    now = datetime.now()
    time_min = now.strftime("%Y-%m-%dT00:00:00+02:00")
    time_max = (now + timedelta(days=days)).strftime("%Y-%m-%dT23:59:59+02:00")

    all_events = []
    for account, info in ACCOUNTS.items():
        token = tokens.get(account)
        if not token:
            continue
        for cal_name, cal_id in info["calendars"].items():
            try:
                events = get_events(token, cal_id, time_min, time_max)
                for e in events:
                    formatted, date_str, day_name, dt = format_event(e, cal_name)
                    if formatted:
                        all_events.append((date_str, day_name, dt, formatted))
            except Exception as ex:
                print(f"  ⚠ {cal_name} ({account}): {ex}", file=sys.stderr)

    # Sort by datetime
    all_events.sort(key=lambda x: x[2])

    # Group by date
    grouped = {}
    for date_str, day_name, dt, line in all_events:
        if date_str not in grouped:
            grouped[date_str] = {"day_name": day_name, "events": []}
        grouped[date_str]["events"].append(line)

    return grouped


def render_output(grouped, days):
    """Render grouped events to markdown."""
    now = datetime.now()
    all_cal_names = [name for info in ACCOUNTS.values() for name in info["calendars"]]
    lines = [
        f"# Google Calendar — przegląd {days} dni",
        f"Pobrano: {now.strftime('%Y-%m-%d %H:%M')} | Konta: {', '.join(ACCOUNTS.keys())}",
        f"Kalendarze: {', '.join(all_cal_names)}",
        "",
    ]

    if not grouped:
        lines.append("Brak wydarzeń w podanym okresie.")
        return "\n".join(lines)

    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    for date_str in sorted(grouped.keys()):
        info = grouped[date_str]
        day_label = info["day_name"]

        if date_str == today:
            marker = " ← DZIŚ"
        elif date_str == tomorrow:
            marker = " ← JUTRO"
        else:
            marker = ""

        lines.append(f"## {day_label} {date_str}{marker}")
        for event_line in info["events"]:
            lines.append(event_line)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Calendar Sync — DOKODU BRAIN")
    parser.add_argument("--pull", action="store_true", help="Pobierz eventy")
    parser.add_argument("--days", type=int, default=7, help="Dni do przodu (default: 7)")
    parser.add_argument("--save", action="store_true", help="Zapisz do Calendar_Last_Sync.md")
    parser.add_argument("--create", type=str, help="Tytuł nowego eventu")
    parser.add_argument("--date", type=str, help="Data eventu (YYYY-MM-DD)")
    parser.add_argument("--time", type=str, help="Godzina eventu (HH:MM)")
    parser.add_argument("--duration", type=int, default=60, help="Czas trwania w minutach (default: 60)")
    parser.add_argument("--calendar", type=str, default=DEFAULT_CALENDAR, help=f"Kalendarz (default: {DEFAULT_CALENDAR})")
    parser.add_argument("--description", type=str, default="", help="Opis eventu")
    args = parser.parse_args()

    if not args.pull and not args.create:
        parser.print_help()
        sys.exit(1)

    print("Calendar Sync — DOKODU BRAIN")
    print("=" * 40)

    # Refresh tokens for all accounts
    tokens = {}
    for account, info in ACCOUNTS.items():
        creds_path = info["creds"]
        if not creds_path.exists():
            print(f"  ⚠ Brak credentials: {account} ({creds_path})")
            continue
        try:
            print(f"  Odświeżam token {account}...", end=" ")
            tokens[account] = refresh_token(creds_path)
            print("✓")
        except Exception as ex:
            print(f"✗ ({ex})")

    if not tokens:
        print("ERROR: Brak aktywnych tokenów!", file=sys.stderr)
        sys.exit(1)

    if args.create:
        if not args.date or not args.time:
            print("ERROR: --create wymaga --date i --time", file=sys.stderr)
            sys.exit(1)

        cal_id = ALL_CALENDARS.get(args.calendar)
        if not cal_id:
            print(f"ERROR: Nieznany kalendarz '{args.calendar}'", file=sys.stderr)
            print(f"Dostępne: {', '.join(ALL_CALENDARS.keys())}", file=sys.stderr)
            sys.exit(1)

        # Find which account owns this calendar
        account = CALENDAR_ACCOUNT[args.calendar]
        token = tokens.get(account)
        if not token:
            print(f"ERROR: Brak tokena dla konta {account}", file=sys.stderr)
            sys.exit(1)

        print(f"\n  Tworzę event: {args.create}")
        print(f"  Data: {args.date} {args.time} ({args.duration} min)")
        print(f"  Kalendarz: {args.calendar} ({account})")

        event = create_event(
            token, cal_id, args.create,
            args.date, args.time, args.duration, args.description,
        )
        print(f"\n  ✅ Utworzono: {event.get('htmlLink', '—')}")

    if args.pull:
        print(f"\n  Pobieram eventy ({args.days} dni)...")
        grouped = pull_events(tokens, args.days)
        output = render_output(grouped, args.days)
        print()
        print(output)

        if args.save:
            SYNC_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            SYNC_OUTPUT.write_text(output + "\n")
            print(f"\n  ✅ Zapisano: {SYNC_OUTPUT}")


if __name__ == "__main__":
    main()
