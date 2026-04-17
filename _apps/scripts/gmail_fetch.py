#!/usr/bin/env python3
"""
DOKODU BRAIN — Gmail Intelligence
Autor: Kacper Sieradzinski | Dokodu sp. z o.o.

Pobiera emaile z Gmail, kategoryzuje i aktualizuje BRAIN.
Wyniki trafiają do DOKODU_BRAIN/20_AREAS/AREA_Email/.

Użycie:
  python3 gmail_fetch.py              # ostatnie 2 dni, zapisz do BRAIN
  python3 gmail_fetch.py --days 7     # ostatnie 7 dni
  python3 gmail_fetch.py --dry-run    # tylko pokaż, nie zapisuj
  python3 gmail_fetch.py --setup      # instrukcja pierwszego uruchomienia
"""

import os
import sys
import json
import pickle
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR   = Path(__file__).parent.resolve()
BRAIN_DIR    = SCRIPT_DIR.parent
CONFIG_DIR   = Path.home() / ".config" / "dokodu"
CREDENTIALS_FILE = CONFIG_DIR / "gmail_credentials.json"
TOKEN_FILE       = CONFIG_DIR / "gmail_token.pickle"
EMAIL_DIR        = BRAIN_DIR / "20_AREAS" / "AREA_Email"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# ══════════════════════════════════════════════
# FILTRY — co ignorować
# ══════════════════════════════════════════════

SPAM_SENDERS = {
    "temu", "allegro", "samsung", "travelist", "uber", "ubereats",
    "netflix", "letyshops", "ceneo", "leroymerlin", "vitay", "erli",
    "morele", "rtveuroagd", "pyszne", "toogoodtogo", "bookbeat",
    "samsung", "samsungusa", "alerabat", "pakolorente", "sts",
    "liviation", "livenation", "virtualvocations", "quora",
    "indieniche", "substack", "beehiiv", "mail.beehiiv",
    "minimalisthustler", "godofprompt", "neilpatel", "zipwp",
}

SPAM_KEYWORDS_SUBJECT = [
    "promocja", "rabat", "zniżka", "wyprzedaż", "gratis", "cashback",
    "oferta", "tylko dziś", "ostatnia szansa", "wygasa",
    "kup teraz", "zamów", "wypróbuj", "darmow",
]

KNOWN_CLIENTS = [
    "corleonis.pl", "animex", "aihero.pl",
]

FINANCIAL_SENDERS = [
    "biuro@saldeo.pl", "pmksiegowosc.pl", "tpay.com",
    "googleplay-noreply@google.com", "payments-noreply@google.com",
    "awizo@mojefinanseplay.pl", "play.pl", "midjourney.com",
    "revolut.com", "skrill.com",
]

OPERATIONAL_SENDERS = [
    "ahrefs.com", "sc-noreply@google.com", "googlebase-noreply@google.com",
    "aftermarket.pl", "cloudflare.com", "notify.cloudflare.com",
    "consentmanager.net", "automat@dns.pl", "dhosting.pl",
    "ingksiegowosc.pl", "mbank.pl",
]

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: Brak bibliotek Google. Zainstaluj:")
    print("  pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)


# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"BRAK: {CREDENTIALS_FILE}")
                print("Uruchom: python3 gmail_fetch.py --setup")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return creds


# ══════════════════════════════════════════════
# POBIERANIE EMAILI
# ══════════════════════════════════════════════

def fetch_emails(service, days: int = 2) -> list[dict]:
    since = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")
    query = f"after:{since}"

    results = service.users().messages().list(
        userId="me", q=query, maxResults=200
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        try:
            full = service.users().messages().get(
                userId="me", id=msg["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()

            headers = {h["name"]: h["value"] for h in full["payload"]["headers"]}
            emails.append({
                "id": msg["id"],
                "subject": headers.get("Subject", "(brak tematu)"),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": full.get("snippet", ""),
            })
        except Exception:
            continue

    return emails


# ══════════════════════════════════════════════
# KATEGORYZACJA
# ══════════════════════════════════════════════

def extract_email_address(from_field: str) -> str:
    match = re.search(r"<(.+?)>", from_field)
    return match.group(1).lower() if match else from_field.lower()


def extract_domain(email: str) -> str:
    return email.split("@")[-1] if "@" in email else email


def is_spam(email: dict) -> bool:
    from_addr = extract_email_address(email["from"]).lower()
    domain = extract_domain(from_addr)
    subject = email["subject"].lower()

    # Znane spamowe domeny
    for spam in SPAM_SENDERS:
        if spam in domain or spam in from_addr:
            return True

    # noreply / newsletter
    if any(x in from_addr for x in ["noreply", "no-reply", "newsletter", "promo@", "marketing@"]):
        return True

    # Spamowe słowa w temacie
    for kw in SPAM_KEYWORDS_SUBJECT:
        if kw in subject:
            return True

    return False


def categorize(email: dict) -> str:
    from_addr = extract_email_address(email["from"]).lower()
    domain = extract_domain(from_addr)
    subject = email["subject"].lower()
    snippet = email["snippet"].lower()

    # LinkedIn
    if "linkedin.com" in from_addr:
        return "linkedin"

    # Klienci aktywni
    for client in KNOWN_CLIENTS:
        if client in domain:
            return "klient"

    # Finansowe
    for sender in FINANCIAL_SENDERS:
        if sender in from_addr:
            return "finansowe"
    if any(w in subject or w in snippet for w in ["faktura", "invoice", "płatność", "rozliczenie", "podatek", "zus"]):
        return "finansowe"

    # Operacyjne
    for sender in OPERATIONAL_SENDERS:
        if sender in from_addr:
            return "operacyjne"
    if any(w in subject for w in ["alert", "error", "wygasa", "expires", "domain", "audit", "orphan", "redirect"]):
        return "operacyjne"

    # Kalendarze / spotkania
    if "calendar-notification@google.com" in from_addr or "zaakceptowano:" in subject or "zaproszenie:" in subject:
        return "kalendarz"

    # Lead — direct non-spam email (nie newsletter, nie noreply)
    if not any(x in from_addr for x in ["@google.com", "@microsoft.com", "@apple.com",
                                          "@amazon.com", "@meta.com", "@github.com"]):
        return "lead"

    return "inne"


def is_polish_name(name: str) -> bool:
    """Heurystyka: polskie imię = ma polskie znaki lub jest w typowym formacie."""
    polish_chars = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")
    if any(c in polish_chars for c in name):
        return True
    # Typowy format: "Imię Nazwisko" (dwa słowa, wielka litera)
    parts = name.strip().split()
    if len(parts) == 2 and all(p[0].isupper() for p in parts if p):
        return True
    return False


def extract_sender_name(from_field: str) -> str:
    match = re.match(r'^"?([^"<]+)"?\s*<', from_field)
    return match.group(1).strip() if match else from_field.split("<")[0].strip()


# ══════════════════════════════════════════════
# FORMATOWANIE RAPORTU
# ══════════════════════════════════════════════

def build_report(emails: list[dict], days: int) -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    categories = {
        "lead": [], "klient": [], "finansowe": [],
        "operacyjne": [], "linkedin": [], "kalendarz": [], "inne": []
    }

    for email in emails:
        if is_spam(email):
            continue
        cat = categorize(email)
        categories[cat].append(email)

    # LinkedIn — tylko polskie imiona
    polish_linkedin = []
    for e in categories["linkedin"]:
        name = extract_sender_name(e["from"])
        name_clean = re.sub(r"\s+via LinkedIn.*", "", name).strip()
        if is_polish_name(name_clean):
            polish_linkedin.append({"name": name_clean, "subject": e["subject"], "date": e["date"]})

    return {
        "date": today,
        "since": since,
        "days": days,
        "total_raw": len(emails),
        "leads": categories["lead"],
        "klienci": categories["klient"],
        "finansowe": categories["finansowe"],
        "operacyjne": categories["operacyjne"],
        "linkedin_pl": polish_linkedin,
        "kalendarz": categories["kalendarz"],
    }


# ══════════════════════════════════════════════
# ZAPIS DO BRAIN
# ══════════════════════════════════════════════

def save_last_sync(report: dict):
    today = report["date"]
    lines = [
        "---",
        "type: sync-log",
        "status: active",
        f"last_sync: {today}",
        f"sync_period: last_{report['days']}_days",
        "---",
        "",
        f"# EMAIL SYNC — OSTATNI RAPORT",
        "",
        f"**Sync:** {today} | **Zakres:** ostatnie {report['days']} dni (od {report['since']})",
        f"**Emaili przeanalizowanych:** {report['total_raw']} | **Po filtrowaniu:** "
        f"{len(report['leads']) + len(report['klienci']) + len(report['finansowe']) + len(report['operacyjne'])} biznesowych",
        "",
        "---",
        "",
    ]

    # Leady
    lines += ["## 🎯 NOWE LEADY B2B", ""]
    if report["leads"]:
        for e in report["leads"][:10]:
            lines.append(f"- **{extract_sender_name(e['from'])}** — {e['subject'][:80]}")
    else:
        lines.append("- Brak nowych leadów")
    lines.append("")

    # Klienci
    lines += ["## 👥 KLIENCI", ""]
    if report["klienci"]:
        for e in report["klienci"]:
            lines.append(f"- **{extract_sender_name(e['from'])}** — {e['subject'][:80]}")
    else:
        lines.append("- Brak wiadomości od klientów")
    lines.append("")

    # Finansowe
    lines += ["## 💰 FINANSOWE", ""]
    if report["finansowe"]:
        for e in report["finansowe"]:
            lines.append(f"- **{extract_sender_name(e['from'])}** — {e['subject'][:80]}")
    else:
        lines.append("- Brak")
    lines.append("")

    # Operacyjne
    lines += ["## ⚙️ OPERACYJNE / ALERTY", ""]
    if report["operacyjne"]:
        for e in report["operacyjne"]:
            lines.append(f"- **{extract_sender_name(e['from'])}** — {e['subject'][:80]}")
    else:
        lines.append("- Brak alertów")
    lines.append("")

    # LinkedIn PL
    lines += ["## 🔗 LINKEDIN — nowe połączenia (PL)", ""]
    if report["linkedin_pl"]:
        for p in report["linkedin_pl"]:
            lines.append(f"- {p['name']}")
    else:
        lines.append("- Brak")
    lines.append("")

    path = EMAIL_DIR / "Email_Last_Sync.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ Zapisano: {path}")


def update_intelligence_log(report: dict):
    path = EMAIL_DIR / "Email_Intelligence.md"
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")
    today = report["date"]

    # Policz akcje
    leads_count = len(report["leads"])
    alerts = len([e for e in report["operacyjne"] if any(
        w in e["subject"].lower() for w in ["wygasa", "expires", "error", "alert", "broken"]
    )])

    new_row = f"| {today} | {leads_count} nowych | {alerts} alertów | sync ok |"

    if "| Data | Nowe B2B |" in content:
        content = content.replace(
            "| Data | Nowe B2B | Akcje | Alerty |",
            "| Data | Nowe B2B | Akcje | Alerty |",
        )
        # Dopisz na końcu tabeli monitoringu
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "| Data | Nowe B2B |" in line:
                # Znajdź koniec tabeli
                j = i + 1
                while j < len(lines) and lines[j].startswith("|"):
                    j += 1
                lines.insert(j, new_row)
                break
        content = "\n".join(lines)
        path.write_text(content, encoding="utf-8")
        print(f"✓ Zaktualizowano log w: {path}")


# ══════════════════════════════════════════════
# SETUP GUIDE
# ══════════════════════════════════════════════

def print_setup():
    print("""
╔══════════════════════════════════════════════════════╗
║         GMAIL FETCH — PIERWSZE URUCHOMIENIE          ║
╚══════════════════════════════════════════════════════╝

1. Wejdź na: https://console.cloud.google.com/
2. Wybierz projekt (ten sam co dla GSC/YouTube)
3. APIs & Services → Enable APIs → włącz "Gmail API"
4. APIs & Services → Credentials → pobierz credentials.json
   (typ: OAuth 2.0 Desktop App)
5. Zapisz jako: ~/.config/dokodu/gmail_credentials.json
6. Uruchom: python3 gmail_fetch.py
   → otworzy się przeglądarka do autoryzacji Gmail

Po autoryzacji token jest zapisany lokalnie — kolejne runy
działają bez przeglądarki.
""")


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="DOKODU Gmail Intelligence")
    parser.add_argument("--days", type=int, default=2, help="Liczba dni wstecz (domyślnie 2)")
    parser.add_argument("--dry-run", action="store_true", help="Tylko pokaż, nie zapisuj")
    parser.add_argument("--setup", action="store_true", help="Pokaż instrukcję konfiguracji")
    args = parser.parse_args()

    if args.setup:
        print_setup()
        return

    print(f"[{datetime.now().strftime('%H:%M')}] Gmail sync start (ostatnie {args.days} dni)...")

    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    print("  → Pobieranie emaili...")
    emails = fetch_emails(service, days=args.days)
    print(f"  → Pobrano {len(emails)} emaili")

    report = build_report(emails, days=args.days)

    # Podsumowanie
    print(f"  → Leady B2B:    {len(report['leads'])}")
    print(f"  → Klienci:      {len(report['klienci'])}")
    print(f"  → Finansowe:    {len(report['finansowe'])}")
    print(f"  → Operacyjne:   {len(report['operacyjne'])}")
    print(f"  → LinkedIn PL:  {len(report['linkedin_pl'])}")

    if args.dry_run:
        print("\n[DRY RUN] Nie zapisuję plików.")
        # Pokaż leady
        if report["leads"]:
            print("\nLeady:")
            for e in report["leads"][:5]:
                print(f"  • {e['from'][:50]} — {e['subject'][:60]}")
        return

    EMAIL_DIR.mkdir(parents=True, exist_ok=True)
    save_last_sync(report)
    update_intelligence_log(report)

    print(f"[{datetime.now().strftime('%H:%M')}] Gmail sync zakończony ✓")


if __name__ == "__main__":
    main()
