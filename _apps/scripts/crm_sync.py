#!/usr/bin/env python3
"""
crm_sync.py — Bidirectional sync between DOKODU_BRAIN (Markdown) and CRM (API).

Usage:
  python scripts/crm_sync.py push-meeting <client_name>     # BRAIN → CRM: push latest meeting
  python scripts/crm_sync.py push-lead <company_name>        # BRAIN → CRM: push lead from CRM_Leady_B2B.md
  python scripts/crm_sync.py push-activity <client_name> <type> <subject>  # Log activity
  python scripts/crm_sync.py pull-pipeline                    # CRM → BRAIN: update CRM_Leady_B2B.md
  python scripts/crm_sync.py pull-company <company_name>      # CRM → BRAIN: update customer Profile.md
  python scripts/crm_sync.py status                           # Show sync status

Config: ~/.config/dokodu/crm_api_key  (or env CRM_API_KEY)
        ~/.config/dokodu/crm_base_url (or env CRM_BASE_URL, default: https://system.dokodu.it)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote

BRAIN_ROOT = Path(__file__).resolve().parent.parent
CUSTOMERS_DIR = BRAIN_ROOT / "20_AREAS" / "AREA_Customers"
CRM_LEADY_PATH = BRAIN_ROOT / "20_AREAS" / "AREA_Marketing_Sales" / "CRM_Leady_B2B.md"


def get_config():
    api_key = os.environ.get("CRM_API_KEY")
    if not api_key:
        key_path = Path.home() / ".config" / "dokodu" / "crm_api_key"
        if key_path.exists():
            api_key = key_path.read_text().strip()
    if not api_key:
        print("ERROR: No CRM API key. Set CRM_API_KEY or create ~/.config/dokodu/crm_api_key")
        sys.exit(1)

    base_url = os.environ.get("CRM_BASE_URL")
    if not base_url:
        url_path = Path.home() / ".config" / "dokodu" / "crm_base_url"
        if url_path.exists():
            base_url = url_path.read_text().strip()
    base_url = base_url or "https://system.dokodu.it"

    return api_key, base_url.rstrip("/")


def api_call(method, endpoint, data=None):
    """Make an authenticated API call to CRM."""
    api_key, base_url = get_config()
    url = f"{base_url}/api{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, method=method)
    req.add_header("X-API-Key", api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"API Error {e.code}: {error_body}")
        sys.exit(1)


# ─── BRAIN → CRM ──────────────────────────────────────

def push_meeting(client_name):
    """Read latest meeting from BRAIN Meetings.md and push to CRM as Activity."""
    client_dir = find_client_dir(client_name)
    if not client_dir:
        print(f"ERROR: Client directory not found for '{client_name}'")
        sys.exit(1)

    meetings_file = client_dir / "Meetings.md"
    if not meetings_file.exists():
        print(f"ERROR: {meetings_file} not found")
        sys.exit(1)

    content = meetings_file.read_text()

    # Parse last meeting (## header with date)
    meetings = re.split(r"^## ", content, flags=re.MULTILINE)
    if len(meetings) < 2:
        print("No meetings found in file")
        sys.exit(1)

    last_meeting = meetings[-1]
    lines = last_meeting.strip().split("\n")
    title = lines[0].strip()

    # Extract date from title (expects format like "2026-04-01 — Discovery Call")
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", title)
    happened_at = (
        date_match.group(1) + "T10:00:00Z"
        if date_match
        else datetime.now().isoformat()
    )

    description = "\n".join(lines[1:]).strip()

    # Find company in CRM
    company = find_crm_company(client_name)
    if not company:
        print(f"Company '{client_name}' not found in CRM. Create it first.")
        sys.exit(1)

    result = api_call(
        "POST",
        "/activities",
        {
            "type": "MEETING",
            "subject": title,
            "description": description[:10000],
            "companyId": company["id"],
            "happenedAt": happened_at,
        },
    )

    print(f"OK: Meeting pushed to CRM (activity ID: {result.get('id', 'unknown')})")


def push_lead(company_name):
    """Push lead data from BRAIN to CRM as Company."""
    if not CRM_LEADY_PATH.exists():
        print(f"ERROR: {CRM_LEADY_PATH} not found")
        sys.exit(1)

    # Check if already exists in CRM
    existing = find_crm_company(company_name)
    if existing:
        print(f"Company '{company_name}' already exists in CRM (ID: {existing['id']})")
        return

    result = api_call(
        "POST",
        "/companies",
        {
            "name": company_name,
            "source": "MANUAL",
        },
    )
    print(f"OK: Company '{company_name}' pushed to CRM (ID: {result.get('id', 'unknown')})")


def push_activity(client_name, activity_type, subject):
    """Log an activity for a company in CRM."""
    company = find_crm_company(client_name)
    if not company:
        print(f"Company '{client_name}' not found in CRM")
        sys.exit(1)

    result = api_call(
        "POST",
        "/activities",
        {
            "type": activity_type.upper(),
            "subject": subject,
            "companyId": company["id"],
            "happenedAt": datetime.now().isoformat(),
        },
    )
    print(f"OK: Activity logged (ID: {result.get('id', 'unknown')})")


# ─── CRM → BRAIN ──────────────────────────────────────

def pull_pipeline():
    """Pull deal pipeline from CRM and update CRM_Leady_B2B.md."""
    deals = api_call("GET", "/deals?pageSize=100")
    data = deals.get("data", [])

    if not data:
        print("No deals found in CRM")
        return

    # Group by stage
    stages = {}
    for deal in data:
        stage_name = deal.get("stage", {}).get("name", "Unknown")
        if stage_name not in stages:
            stages[stage_name] = []
        stages[stage_name].append(deal)

    # Generate markdown
    now = datetime.now().strftime("%Y-%m-%d")
    now_full = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "---",
        "type: area",
        "status: active",
        "owner: Kacper",
        f"last_reviewed: {now}",
        "tags: [crm, pipeline, b2b]",
        "---",
        "",
        "# CRM Leady B2B",
        "",
        f"> Ostatnia synchronizacja z CRM: {now_full}",
        "",
    ]

    for stage_name, stage_deals in stages.items():
        lines.append(f"## {stage_name}")
        lines.append("")
        lines.append("| Firma | Deal | Wartość | Typ | Assigned | Data |")
        lines.append("|-------|------|---------|-----|----------|------|")
        for d in stage_deals:
            company = d.get("company", {}).get("name", "-")
            title = d.get("title", "-")
            value = d.get("value") or "-"
            deal_type = d.get("dealType", "-")
            assigned = (
                d.get("assignedTo", {}).get("name", "-")
                if d.get("assignedTo")
                else "-"
            )
            date = d.get("expectedCloseDate", "-")
            if date and date != "-":
                date = date[:10]
            lines.append(
                f"| {company} | {title} | {value} PLN | {deal_type} | {assigned} | {date} |"
            )
        lines.append("")

    CRM_LEADY_PATH.write_text("\n".join(lines))
    print(f"OK: CRM_Leady_B2B.md updated with {len(data)} deals")


def pull_company(company_name):
    """Pull company data from CRM and update BRAIN customer Profile.md."""
    company = find_crm_company(company_name)
    if not company:
        print(f"Company '{company_name}' not found in CRM")
        sys.exit(1)

    # Get full company details
    details = api_call("GET", f"/companies/{company['id']}")

    client_dir = find_client_dir(company_name)
    if not client_dir:
        # Create directory
        safe_name = re.sub(r"[^\w\-]", "_", company_name)
        client_dir = CUSTOMERS_DIR / safe_name
        client_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {client_dir}")

    profile_path = client_dir / "Profile.md"
    now = datetime.now().strftime("%Y-%m-%d")
    now_full = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "---",
        "type: customer",
        f"status: {(details.get('status') or 'CONTACT').lower()}",
        "owner: Kacper",
        f"last_reviewed: {now}",
        f"crm_id: {details.get('id', '')}",
        f"tags: [{details.get('industry') or 'unknown'}]",
        "---",
        "",
        f"# {details.get('name', company_name)}",
        "",
        "## Dane firmy",
        "",
        f"- **NIP:** {details.get('nip') or '-'}",
        f"- **Branża:** {details.get('industry') or '-'}",
        f"- **Wielkość:** {details.get('size') or '-'}",
        f"- **Miasto:** {details.get('city') or '-'}",
        f"- **Strona:** {details.get('website') or '-'}",
        f"- **LinkedIn:** {details.get('linkedinUrl') or '-'}",
        f"- **ICP Score:** {details.get('icpScore') or '-'}",
        f"- **Źródło:** {details.get('source') or '-'}",
        "",
        "## Kontakty",
        "",
    ]

    contacts = details.get("contacts", [])
    for c in contacts:
        lines.append(
            f"- **{c.get('firstName', '')} {c.get('lastName', '')}** — {c.get('position') or '-'}"
        )
        if c.get("email"):
            lines.append(f"  - Email: {c['email']}")
        if c.get("phone"):
            lines.append(f"  - Tel: {c['phone']}")

    lines.append("")
    lines.append("## Notatki")
    lines.append("")
    lines.append(f"> Zsynchronizowano z CRM: {now_full}")
    lines.append("")

    profile_path.write_text("\n".join(lines))
    print(f"OK: {profile_path} updated from CRM")


def show_status():
    """Show sync status — companies in CRM vs BRAIN."""
    companies = api_call("GET", "/companies?pageSize=100")
    crm_names = {c["name"] for c in companies.get("data", [])}

    brain_dirs = set()
    if CUSTOMERS_DIR.exists():
        brain_dirs = {d.name for d in CUSTOMERS_DIR.iterdir() if d.is_dir()}

    print(f"CRM companies: {len(crm_names)}")
    print(f"BRAIN customer dirs: {len(brain_dirs)}")

    only_crm = crm_names - brain_dirs
    if only_crm:
        print(f"\nOnly in CRM (not in BRAIN):")
        for name in sorted(only_crm):
            print(f"  - {name}")


# ─── Helpers ──────────────────────────────────────────

def find_client_dir(name):
    """Find customer directory in BRAIN by fuzzy name match."""
    if not CUSTOMERS_DIR.exists():
        return None
    for d in CUSTOMERS_DIR.iterdir():
        if d.is_dir() and name.lower() in d.name.lower():
            return d
    return None


def find_crm_company(name):
    """Search for company in CRM by name."""
    encoded = quote(name)
    result = api_call("GET", f"/search?q={encoded}")
    companies = result.get("companies", [])
    if companies:
        return companies[0]
    return None


def main():
    parser = argparse.ArgumentParser(description="BRAIN <-> CRM bidirectional sync")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show sync status")
    sub.add_parser("pull-pipeline", help="CRM -> BRAIN: update CRM_Leady_B2B.md")

    p = sub.add_parser("push-meeting", help="BRAIN -> CRM: push latest meeting")
    p.add_argument("client_name")

    p = sub.add_parser("push-lead", help="BRAIN -> CRM: push lead as company")
    p.add_argument("company_name")

    p = sub.add_parser(
        "push-activity", help="Log activity for company in CRM"
    )
    p.add_argument("client_name")
    p.add_argument(
        "type",
        choices=[
            "call",
            "email_sent",
            "email_received",
            "meeting",
            "note",
            "linkedin_message",
            "sms",
        ],
    )
    p.add_argument("subject")

    p = sub.add_parser("pull-company", help="CRM -> BRAIN: update Profile.md")
    p.add_argument("company_name")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd = args.command.replace("-", "_")

    if cmd == "status":
        show_status()
    elif cmd == "push_meeting":
        push_meeting(args.client_name)
    elif cmd == "push_lead":
        push_lead(args.company_name)
    elif cmd == "push_activity":
        push_activity(args.client_name, args.type, args.subject)
    elif cmd == "pull_pipeline":
        pull_pipeline()
    elif cmd == "pull_company":
        pull_company(args.company_name)


if __name__ == "__main__":
    main()
