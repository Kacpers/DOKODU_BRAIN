# CRM ↔ BRAIN Bidirectional Sync — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bidirectional near real-time sync between DOKODU_BRAIN (markdown, git) and Dokodu CRM (Next.js + PostgreSQL) so team members without CLI access can track and interact with business data.

**Architecture:** Sync daemon (Python) runs on VPS every 5 min. BRAIN→CRM parses markdown diffs and pushes to CRM API. CRM→BRAIN reads change feed and commits to git. Identity mapping via `crm_id` in markdown + `.sync_mapping.json`. Sync markers in MD files protect non-synced sections.

**Tech Stack:** Python 3 (daemon), Next.js/TypeScript (CRM), Prisma/PostgreSQL (DB), systemd (service), ruamel.yaml (YAML parsing)

**Spec:** `docs/superpowers/specs/2026-04-02-crm-brain-sync-design.md`

**Repos:**
- CRM app: `/home/kacper/DOKODU/CRM` (Next.js, deploys to system.dokodu.it)
- BRAIN: `/home/kacper/DOKODU_BRAIN` (markdown, git)
- Daemon: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/` (new, deployed to VPS)

---

## Phase 1: CRM Backend — Change Tracking

### Task 1: Add ChangeLog model to Prisma schema

**Files:**
- Modify: `/home/kacper/DOKODU/CRM/prisma/schema.prisma`

- [ ] **Step 1: Add ChangeLog model to schema**

Add after the AuditLog model in `schema.prisma`:

```prisma
model ChangeLog {
  id          String   @id @default(cuid())
  entity      String   // "deal", "company", "contact", "activity", "task"
  entityId    String
  action      String   // "create", "update", "delete"
  fields      Json     // changed fields with new values
  metadata    Json?    // extra context (previousStage, etc.)
  userId      String?
  user        User?    @relation("ChangeLogUser", fields: [userId], references: [id])
  timestamp   DateTime @default(now())

  @@index([timestamp])
  @@index([entity, entityId])
}
```

Also add to the User model relations:

```prisma
changeLogs    ChangeLog[] @relation("ChangeLogUser")
```

- [ ] **Step 2: Push schema to database**

```bash
cd /home/kacper/DOKODU/CRM && npx prisma db push
```

Expected: "Your database is now in sync with your Prisma schema."

- [ ] **Step 3: Generate Prisma client**

```bash
cd /home/kacper/DOKODU/CRM && npx prisma generate
```

- [ ] **Step 4: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add prisma/schema.prisma && git commit -m "feat: add ChangeLog model for sync daemon"
```

---

### Task 2: Create change logging utility

**Files:**
- Create: `/home/kacper/DOKODU/CRM/src/lib/change-log.ts`

- [ ] **Step 1: Create change-log.ts**

```typescript
import { db } from "@/lib/prisma";

type ChangeEntity = "deal" | "company" | "contact" | "activity" | "task";

interface LogChangeParams {
  entity: ChangeEntity;
  entityId: string;
  action: "create" | "update" | "delete";
  fields: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  userId?: string;
}

export async function logChange(params: LogChangeParams): Promise<void> {
  try {
    await db.changeLog.create({
      data: {
        entity: params.entity,
        entityId: params.entityId,
        action: params.action,
        fields: params.fields,
        metadata: params.metadata ?? undefined,
        userId: params.userId ?? undefined,
      },
    });
  } catch (error) {
    console.error("[ChangeLog] Failed to log change:", error);
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/lib/change-log.ts && git commit -m "feat: add change logging utility for sync"
```

---

### Task 3: Wire change logging into existing API routes

**Files:**
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/deals/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/deals/[id]/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/deals/[id]/stage/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/companies/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/companies/[id]/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/contacts/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/contacts/[id]/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/activities/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/tasks/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/tasks/[id]/route.ts`
- Modify: `/home/kacper/DOKODU/CRM/src/app/api/tasks/[id]/complete/route.ts`

For each route: add `import { logChange } from "@/lib/change-log"` and call `logChange()` after successful create/update/delete operations. Pattern:

- [ ] **Step 1: Add logChange to deals POST (create)**

In `/home/kacper/DOKODU/CRM/src/app/api/deals/route.ts`, after the `prisma.deal.create()` call and before the return, add:

```typescript
import { logChange } from "@/lib/change-log";

// After: const deal = await prisma.deal.create(...)
logChange({
  entity: "deal",
  entityId: deal.id,
  action: "create",
  fields: { title: deal.title, value: deal.value?.toString(), stageId: deal.stageId, companyId: deal.companyId },
  userId: session.user.id,
});
```

- [ ] **Step 2: Add logChange to deals PATCH (update)**

In `/home/kacper/DOKODU/CRM/src/app/api/deals/[id]/route.ts`, after `prisma.deal.update()`:

```typescript
logChange({
  entity: "deal",
  entityId: deal.id,
  action: "update",
  fields: validated.data,
  userId: session.user.id,
});
```

- [ ] **Step 3: Add logChange to deals stage change**

In `/home/kacper/DOKODU/CRM/src/app/api/deals/[id]/stage/route.ts`, after stage update:

```typescript
logChange({
  entity: "deal",
  entityId: params.id,
  action: "update",
  fields: { stageId: newStageId },
  metadata: { previousStageId: previousStageId, stageName: newStage.name },
  userId: session.user.id,
});
```

- [ ] **Step 4: Add logChange to companies POST/PATCH/DELETE**

Same pattern in `/api/companies/route.ts` (POST) and `/api/companies/[id]/route.ts` (PATCH, DELETE):

```typescript
logChange({
  entity: "company",
  entityId: company.id,
  action: "create", // or "update" or "delete"
  fields: { name: company.name, status: company.status, ...changedFields },
  userId: session.user.id,
});
```

- [ ] **Step 5: Add logChange to contacts POST/PATCH/DELETE**

Same pattern in `/api/contacts/route.ts` and `/api/contacts/[id]/route.ts`.

- [ ] **Step 6: Add logChange to activities POST**

In `/api/activities/route.ts` after create:

```typescript
logChange({
  entity: "activity",
  entityId: activity.id,
  action: "create",
  fields: { type: activity.type, subject: activity.subject, companyId: activity.companyId, dealId: activity.dealId },
  userId: session.user.id,
});
```

- [ ] **Step 7: Add logChange to tasks POST/PATCH/complete**

Same pattern in `/api/tasks/route.ts`, `/api/tasks/[id]/route.ts`, `/api/tasks/[id]/complete/route.ts`.

- [ ] **Step 8: Test by creating a deal in CRM UI, then check DB**

```bash
# After creating a deal in the CRM web UI:
cd /home/kacper/DOKODU/CRM && npx prisma studio
# Check ChangeLog table — should have a new entry
```

- [ ] **Step 9: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/app/api/deals/ src/app/api/companies/ src/app/api/contacts/ src/app/api/activities/ src/app/api/tasks/ && git commit -m "feat: wire change logging into all core API routes"
```

---

### Task 4: Create `/api/changes` endpoint

**Files:**
- Create: `/home/kacper/DOKODU/CRM/src/app/api/changes/route.ts`

- [ ] **Step 1: Create the endpoint**

```typescript
import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/prisma";
import { requireApiKey, errorResponse } from "@/lib/auth-helpers";

export async function GET(request: NextRequest) {
  try {
    await requireApiKey(request);
  } catch (error) {
    return errorResponse(error);
  }

  const { searchParams } = new URL(request.url);
  const since = searchParams.get("since");
  const limit = parseInt(searchParams.get("limit") || "100", 10);

  if (!since) {
    return NextResponse.json({ error: "Missing 'since' parameter (ISO timestamp)" }, { status: 400 });
  }

  const sinceDate = new Date(since);
  if (isNaN(sinceDate.getTime())) {
    return NextResponse.json({ error: "Invalid 'since' timestamp" }, { status: 400 });
  }

  const changes = await db.changeLog.findMany({
    where: { timestamp: { gt: sinceDate } },
    orderBy: { timestamp: "asc" },
    take: Math.min(limit, 500),
    include: { user: { select: { name: true, email: true } } },
  });

  const syncCursor = changes.length > 0
    ? changes[changes.length - 1].timestamp.toISOString()
    : since;

  return NextResponse.json({
    changes: changes.map((c) => ({
      id: c.id,
      entity: c.entity,
      entityId: c.entityId,
      action: c.action,
      fields: c.fields,
      metadata: c.metadata,
      user: c.user?.name || c.user?.email || "system",
      timestamp: c.timestamp.toISOString(),
    })),
    syncCursor,
    count: changes.length,
  });
}
```

- [ ] **Step 2: Test with curl**

```bash
# Get the CRM API key
CRM_KEY=$(cat ~/.config/dokodu/crm_api_key)

# Should return empty changes array (nothing since now)
curl -s -H "X-API-Key: $CRM_KEY" "https://system.dokodu.it/api/changes?since=2026-04-01T00:00:00Z" | python3 -m json.tool
```

Expected: `{"changes": [...], "syncCursor": "...", "count": N}`

- [ ] **Step 3: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/app/api/changes/route.ts && git commit -m "feat: add /api/changes endpoint for sync daemon"
```

---

### Task 5: Add sync status endpoint

**Files:**
- Create: `/home/kacper/DOKODU/CRM/src/app/api/sync/status/route.ts`

- [ ] **Step 1: Create sync status endpoint**

```typescript
import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/prisma";

export async function GET(request: NextRequest) {
  // Public endpoint — shows sync health in UI footer

  const lastChange = await db.changeLog.findFirst({
    orderBy: { timestamp: "desc" },
    select: { timestamp: true },
  });

  // Check for a special "sync_heartbeat" entry
  const lastSync = await db.changeLog.findFirst({
    where: { entity: "sync", action: "heartbeat" },
    orderBy: { timestamp: "desc" },
    select: { timestamp: true, metadata: true },
  });

  const now = new Date();
  const lastSyncTime = lastSync?.timestamp;
  const syncHealthy = lastSyncTime
    ? (now.getTime() - lastSyncTime.getTime()) < 15 * 60 * 1000 // 15 min
    : false;

  return NextResponse.json({
    lastSync: lastSyncTime?.toISOString() || null,
    lastChange: lastChange?.timestamp.toISOString() || null,
    healthy: syncHealthy,
    metadata: lastSync?.metadata || null,
  });
}

export async function POST(request: NextRequest) {
  // Called by sync daemon to report heartbeat
  const { requireApiKey, errorResponse } = await import("@/lib/auth-helpers");
  try {
    await requireApiKey(request);
  } catch (error) {
    return errorResponse(error);
  }

  const body = await request.json();

  await db.changeLog.create({
    data: {
      entity: "sync",
      entityId: "daemon",
      action: "heartbeat",
      fields: {},
      metadata: body.metadata || { direction: body.direction || "unknown" },
    },
  });

  return NextResponse.json({ ok: true });
}
```

- [ ] **Step 2: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/app/api/sync/status/route.ts && git commit -m "feat: add /api/sync/status endpoint for monitoring"
```

---

## Phase 2: BRAIN Preparation — Sync Markers

### Task 6: Add sync markers to BRAIN markdown files

**Files:**
- Modify: `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md`
- Modify: `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/Outreach_Tracker.md`

The sync daemon will ONLY regenerate content between sync markers. Everything else (templates, protocols, notes) stays untouched.

- [ ] **Step 1: Add sync markers to CRM_Leady_B2B.md**

Wrap the pipeline table with markers. Find the `## PIPELINE AKTYWNY` section and wrap the table:

```markdown
## PIPELINE AKTYWNY

<!-- SYNC:PIPELINE -->
| # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline |
| :- | :--- | :--- | :--- | :--- | ---: | :--- | :---: |
| 1 | Animex | Kamil Kowalski | ... | ... | ... | ... | ... |
...
<!-- /SYNC:PIPELINE -->

**Pipeline Value (otwarty):** ___ PLN
```

- [ ] **Step 2: Add sync markers to Outreach_Tracker.md**

Wrap the `## Pipeline Aktywny` table:

```markdown
## Pipeline Aktywny

<!-- SYNC:OUTREACH -->
| # | Firma | Osoba | Stanowisko | Score | Data zaproszenia | Status | Następny krok | Follow-up |
...
<!-- /SYNC:OUTREACH -->

## Kolejka (Score A — następne w kolejności)
```

- [ ] **Step 3: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add 20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md 20_AREAS/AREA_Marketing_Sales/Outreach_Tracker.md && git commit -m "feat: add sync markers to pipeline and outreach files"
```

---

## Phase 3: Sync Daemon

### Task 7: Create sync daemon project structure

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/__init__.py`
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/config.py`
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/requirements.txt`

- [ ] **Step 1: Create project structure**

```bash
mkdir -p /home/kacper/DOKODU_BRAIN/scripts/sync_daemon
```

- [ ] **Step 2: Create requirements.txt**

```
requests>=2.31.0
ruamel.yaml>=0.18.0
python-dateutil>=2.8.0
```

- [ ] **Step 3: Create config.py**

```python
"""Sync daemon configuration."""

import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "brain_repo_path": "/srv/dokodu-brain",
    "crm_base_url": "https://system.dokodu.it",
    "crm_api_key_file": str(Path.home() / ".config/dokodu/crm_api_key"),
    "sync_interval_seconds": 300,
    "git_remote": "origin",
    "git_branch": "main",
    "commit_author_name": "BRAIN Sync Daemon",
    "commit_author_email": "sync@dokodu.it",
    "state_file": ".sync_state.json",
    "mapping_file": ".sync_mapping.json",
    "lock_file": "/tmp/dokodu-sync.lock",
    "log_dir": "/var/log/dokodu-sync",
}


def load_config(config_path: str | None = None) -> dict:
    """Load config from file, falling back to defaults."""
    config = DEFAULT_CONFIG.copy()

    path = config_path or os.environ.get(
        "SYNC_CONFIG", str(Path.home() / ".config/dokodu/sync_config.json")
    )

    if Path(path).exists():
        with open(path) as f:
            config.update(json.load(f))

    # Resolve API key
    key_file = Path(config["crm_api_key_file"]).expanduser()
    if key_file.exists():
        config["crm_api_key"] = key_file.read_text().strip()
    else:
        config["crm_api_key"] = os.environ.get("CRM_API_KEY", "")

    return config
```

- [ ] **Step 4: Create __init__.py**

```python
"""DOKODU BRAIN ↔ CRM Sync Daemon."""
```

- [ ] **Step 5: Add sync state files to .gitignore**

Add to `/home/kacper/DOKODU_BRAIN/.gitignore`:
```
.sync_state.json
.sync_mapping.json
```

- [ ] **Step 6: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/ .gitignore && git commit -m "feat: sync daemon project structure and config"
```

---

### Task 8: Build shared markdown parser library

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/brain_parser.py`
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/test_brain_parser.py`

This is the critical piece — parses BRAIN markdown into structured data.

- [ ] **Step 1: Write tests for pipeline parser**

```python
"""Tests for brain_parser.py"""

import pytest
from brain_parser import (
    parse_pipeline_table,
    parse_outreach_table,
    parse_profile_yaml,
    parse_meeting_sections,
    parse_reminders,
    extract_sync_section,
    update_sync_section,
)


SAMPLE_PIPELINE = """## PIPELINE AKTYWNY

<!-- SYNC:PIPELINE -->
| # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline |
| :- | :--- | :--- | :--- | :--- | ---: | :--- | :---: |
| 1 | Animex | Kamil Kowalski | Ref. | WYGRANA | 18 000 | Faktura za szkolenia | 2026-04-07 |
| 2 | Corleonis | [imie] | LinkedIn | WYGRANA | 35 000 | Faza UAT | — |
| 3 | TenderScope | Borys Kowalik | Inbound (dokodu.it) | Kontakt | ~20 000 | Czekamy | 2026-04-03 |
<!-- /SYNC:PIPELINE -->

**Pipeline Value (otwarty):** ___ PLN
"""


def test_extract_sync_section():
    content = extract_sync_section(SAMPLE_PIPELINE, "PIPELINE")
    assert "Animex" in content
    assert "Pipeline Value" not in content


def test_parse_pipeline_table():
    section = extract_sync_section(SAMPLE_PIPELINE, "PIPELINE")
    rows = parse_pipeline_table(section)
    assert len(rows) == 3
    assert rows[0]["firma"] == "Animex"
    assert rows[0]["kontakt"] == "Kamil Kowalski"
    assert rows[0]["etap"] == "WYGRANA"
    assert rows[0]["wartosc"] == "18 000"
    assert rows[2]["firma"] == "TenderScope"


SAMPLE_OUTREACH = """## Pipeline Aktywny

<!-- SYNC:OUTREACH -->
| # | Firma | Osoba | Stanowisko | Score | Data zaproszenia | Status | Następny krok | Follow-up |
|---|-------|-------|-----------|-------|-----------------|--------|---------------|-----------|
| 1 | VTS Group | Rafał Wiatr | CTO | A | 2026-03-30 | zaproszenie_wysłane | Czekaj na akceptację → DM | 2026-04-02 |
| 2a | Rossmann SDP | Małgorzata Kołodziejczyk | IT Director | A | 2026-03-30 | zaproszenie_wysłane | Czekaj | 2026-04-02 |
| 2b | Rossmann SDP | Piotr Jugiel | IT Director | A | 2026-03-30 | zaproszenie_wysłane | Czekaj | 2026-04-02 |
| 2b-note | ↳ Notatka | | | | | | |
<!-- /SYNC:OUTREACH -->
"""


def test_parse_outreach_table():
    section = extract_sync_section(SAMPLE_OUTREACH, "OUTREACH")
    rows = parse_outreach_table(section)
    # Should have 3 contact rows (note-rows excluded)
    assert len(rows) == 3
    assert rows[0]["firma"] == "VTS Group"
    assert rows[1]["firma"] == "Rossmann SDP"
    assert rows[1]["nr"] == "2a"
    # Note row should be skipped
    assert all(r["nr"] != "2b-note" for r in rows)


def test_parse_outreach_groups_by_company():
    section = extract_sync_section(SAMPLE_OUTREACH, "OUTREACH")
    rows = parse_outreach_table(section)
    rossmann_rows = [r for r in rows if r["firma"] == "Rossmann SDP"]
    assert len(rossmann_rows) == 2


SAMPLE_PROFILE = """---
type: customer-profile
status: active
owner: kacper
crm_id: cmp_abc123
last_reviewed: 2026-03-15
tags: [klient, produkcja]
---

# Animex — Profil Klienta

## Dane Firmy
- **Pełna nazwa:** Animex Foods sp. z o.o.
- **NIP:** 5272755027
- **Branża:** Produkcja / BOK
"""


def test_parse_profile_yaml():
    data = parse_profile_yaml(SAMPLE_PROFILE)
    assert data["crm_id"] == "cmp_abc123"
    assert data["status"] == "active"
    assert "klient" in data["tags"]


SAMPLE_MEETINGS = """# Animex — Meetings

## 2026-03-15 — Discovery Call

Uczestnicy: Kamil Kowalski, Kacper
Temat: Diagnoza potrzeb BOK

Kluczowe ustalenia:
- SAP jest głównym systemem
- Potrzebują automatyzacji emaili

## 2026-03-10 — Intro Call

Uczestnicy: Kamil, Kacper
Temat: Pierwsze poznanie
"""


def test_parse_meeting_sections():
    meetings = parse_meeting_sections(SAMPLE_MEETINGS)
    assert len(meetings) == 2
    assert meetings[0]["date"] == "2026-03-15"
    assert meetings[0]["title"] == "Discovery Call"
    assert "SAP" in meetings[0]["content"]
    # Should be sorted newest first
    assert meetings[0]["date"] > meetings[1]["date"]


def test_update_sync_section():
    new_table = """| # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline |
| :- | :--- | :--- | :--- | :--- | ---: | :--- | :---: |
| 1 | Animex | Kamil Kowalski | Ref. | WYGRANA | 18 000 | Faktura | 2026-04-07 |
"""
    result = update_sync_section(SAMPLE_PIPELINE, "PIPELINE", new_table)
    assert "<!-- SYNC:PIPELINE -->" in result
    assert "<!-- /SYNC:PIPELINE -->" in result
    assert "Pipeline Value" in result  # content outside markers preserved
    assert "Corleonis" not in result  # old row removed
    assert "Faktura" in result  # new content present
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/kacper/DOKODU_BRAIN/scripts/sync_daemon && python3 -m pytest test_brain_parser.py -v 2>&1 | head -30
```

Expected: ImportError or collection errors (module doesn't exist yet)

- [ ] **Step 3: Implement brain_parser.py**

```python
"""BRAIN markdown parser — extracts structured data from DOKODU_BRAIN files."""

import re
from typing import Any

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True


# ─── Sync Section Helpers ───


def extract_sync_section(content: str, marker: str) -> str:
    """Extract content between <!-- SYNC:{marker} --> and <!-- /SYNC:{marker} -->."""
    pattern = rf"<!-- SYNC:{marker} -->\n(.*?)<!-- /SYNC:{marker} -->"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"Sync marker SYNC:{marker} not found")
    return match.group(1).strip()


def update_sync_section(content: str, marker: str, new_content: str) -> str:
    """Replace content between sync markers, preserving everything else."""
    pattern = rf"(<!-- SYNC:{marker} -->\n).*?(<!-- /SYNC:{marker} -->)"
    replacement = rf"\g<1>{new_content.strip()}\n\g<2>"
    result = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return result


# ─── Markdown Table Parser ───


def _parse_md_table(text: str, columns: list[str]) -> list[dict[str, str]]:
    """Parse a markdown table into a list of dicts. Skips header and separator rows."""
    rows = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        # Skip header row (contains column names) and separator (contains ---)
        if not cells or any(set(c) <= set("-: ") for c in cells if c):
            continue
        if len(cells) < len(columns):
            cells.extend([""] * (len(columns) - len(cells)))
        row = {col: cells[i] if i < len(cells) else "" for i, col in enumerate(columns)}
        rows.append(row)
    return rows


# ─── Pipeline Parser ───


PIPELINE_COLUMNS = ["nr", "firma", "kontakt", "zrodlo", "etap", "wartosc", "nastepny_krok", "deadline"]


def parse_pipeline_table(section: str) -> list[dict[str, str]]:
    """Parse the pipeline table from a sync section."""
    rows = _parse_md_table(section, PIPELINE_COLUMNS)
    # Filter out empty/placeholder rows
    return [r for r in rows if r["firma"] and r["firma"] != "___"]


# ─── Outreach Parser ───


OUTREACH_COLUMNS = ["nr", "firma", "osoba", "stanowisko", "score", "data_zaproszenia", "status", "nastepny_krok", "follow_up"]


def parse_outreach_table(section: str) -> list[dict[str, str]]:
    """Parse outreach table. Skips note-rows (suffix -note) and empty rows."""
    rows = _parse_md_table(section, OUTREACH_COLUMNS)
    return [
        r for r in rows
        if r["firma"]
        and not r["nr"].endswith("-note")
        and not r["firma"].startswith("↳")
    ]


# ─── Profile YAML Parser ───


def parse_profile_yaml(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from a Profile.md file."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    return dict(yaml.load(match.group(1)) or {})


def update_profile_yaml(content: str, updates: dict[str, Any]) -> str:
    """Update YAML frontmatter fields without touching the rest of the file."""
    match = re.match(r"^(---\n)(.*?)(\n---)", content, re.DOTALL)
    if not match:
        return content

    from io import StringIO

    data = yaml.load(match.group(2)) or {}
    data.update(updates)
    stream = StringIO()
    yaml.dump(data, stream)
    new_yaml = stream.getvalue().rstrip()

    return f"{match.group(1)}{new_yaml}{match.group(3)}{content[match.end():]}"


# ─── Meeting Sections Parser ───


def parse_meeting_sections(content: str) -> list[dict[str, str]]:
    """Parse ## YYYY-MM-DD — Title sections from Meetings.md."""
    pattern = r"^## (\d{4}-\d{2}-\d{2}) — (.+)$"
    meetings = []
    current = None

    for line in content.splitlines():
        match = re.match(pattern, line)
        if match:
            if current:
                meetings.append(current)
            current = {
                "date": match.group(1),
                "title": match.group(2).strip(),
                "content": "",
            }
        elif current is not None:
            current["content"] += line + "\n"

    if current:
        meetings.append(current)

    # Trim content whitespace
    for m in meetings:
        m["content"] = m["content"].strip()

    # Sort newest first
    meetings.sort(key=lambda m: m["date"], reverse=True)
    return meetings


def append_meeting_section(content: str, date: str, title: str, body: str) -> str:
    """Insert a new meeting section in chronological order (newest first, after the H1)."""
    new_section = f"\n## {date} — {title}\n\n{body}\n"

    # Find position after the H1 header line
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 1
            # Skip blank lines after H1
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1
            break

    lines.insert(insert_idx, new_section)
    return "".join(lines)


# ─── Reminders Parser ───


def parse_reminders(content: str) -> list[dict[str, str]]:
    """Parse reminder lines: - YYYY-MM-DD | CATEGORY | Text."""
    pattern = r"^- (\d{4}-\d{2}-\d{2}) \| (\w+) \| (.+)$"
    reminders = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("~~"):
            continue  # Skip completed
        match = re.match(pattern, line)
        if match:
            reminders.append({
                "date": match.group(1),
                "category": match.group(2),
                "text": match.group(3).strip(),
            })
    return reminders
```

- [ ] **Step 4: Run tests**

```bash
cd /home/kacper/DOKODU_BRAIN/scripts/sync_daemon && pip3 install ruamel.yaml pytest && python3 -m pytest test_brain_parser.py -v
```

Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/brain_parser.py scripts/sync_daemon/test_brain_parser.py && git commit -m "feat: brain markdown parser with tests"
```

---

### Task 9: Build CRM API client for daemon

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/crm_client.py`

- [ ] **Step 1: Create CRM API client**

```python
"""CRM API client for sync daemon."""

import logging
import requests
from typing import Any

log = logging.getLogger("sync.crm_client")


class CrmClient:
    """Thin wrapper around Dokodu CRM REST API."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict | list | None:
        url = f"{self.base_url}{path}"
        resp = self.session.request(method, url, **kwargs)
        if resp.status_code >= 400:
            log.error(f"{method} {path} → {resp.status_code}: {resp.text[:300]}")
            resp.raise_for_status()
        if resp.status_code == 204:
            return None
        return resp.json()

    # ─── Changes ───

    def get_changes(self, since: str, limit: int = 100) -> dict:
        return self._request("GET", "/api/changes", params={"since": since, "limit": limit})

    def post_heartbeat(self, direction: str) -> None:
        self._request("POST", "/api/sync/status", json={"direction": direction})

    # ─── Companies ───

    def list_companies(self, page_size: int = 200) -> list[dict]:
        data = self._request("GET", "/api/companies", params={"pageSize": page_size})
        return data.get("data", []) if isinstance(data, dict) else data

    def create_company(self, data: dict) -> dict:
        return self._request("POST", "/api/companies", json=data)

    def update_company(self, company_id: str, data: dict) -> dict:
        return self._request("PATCH", f"/api/companies/{company_id}", json=data)

    def search(self, query: str) -> list[dict]:
        data = self._request("GET", "/api/search", params={"q": query})
        return data if isinstance(data, list) else data.get("results", [])

    # ─── Deals ───

    def list_deals(self, page_size: int = 200) -> list[dict]:
        data = self._request("GET", "/api/deals", params={"pageSize": page_size})
        return data.get("data", []) if isinstance(data, dict) else data

    def create_deal(self, data: dict) -> dict:
        return self._request("POST", "/api/deals", json=data)

    def update_deal(self, deal_id: str, data: dict) -> dict:
        return self._request("PATCH", f"/api/deals/{deal_id}", json=data)

    def update_deal_stage(self, deal_id: str, stage_id: str) -> dict:
        return self._request("PATCH", f"/api/deals/{deal_id}/stage", json={"stageId": stage_id})

    # ─── Contacts ───

    def list_contacts(self, page_size: int = 200) -> list[dict]:
        data = self._request("GET", "/api/contacts", params={"pageSize": page_size})
        return data.get("data", []) if isinstance(data, dict) else data

    def create_contact(self, data: dict) -> dict:
        return self._request("POST", "/api/contacts", json=data)

    def update_contact(self, contact_id: str, data: dict) -> dict:
        return self._request("PATCH", f"/api/contacts/{contact_id}", json=data)

    # ─── Activities ───

    def create_activity(self, data: dict) -> dict:
        return self._request("POST", "/api/activities", json=data)

    # ─── Tasks ───

    def create_task(self, data: dict) -> dict:
        return self._request("POST", "/api/tasks", json=data)

    def complete_task(self, task_id: str) -> dict:
        return self._request("PATCH", f"/api/tasks/{task_id}/complete", json={})

    # ─── Pipeline stages ───

    def list_pipeline_stages(self) -> list[dict]:
        data = self._request("GET", "/api/pipelines")
        if isinstance(data, dict) and "data" in data:
            pipelines = data["data"]
        elif isinstance(data, list):
            pipelines = data
        else:
            return []
        stages = []
        for p in pipelines:
            for s in p.get("stages", []):
                stages.append(s)
        return stages
```

- [ ] **Step 2: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/crm_client.py && git commit -m "feat: CRM API client for sync daemon"
```

---

### Task 10: Build identity mapping manager

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/identity.py`

- [ ] **Step 1: Create identity mapping module**

```python
"""Identity mapping between BRAIN paths/names and CRM IDs."""

import json
import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger("sync.identity")


class IdentityMap:
    """Manages stable identity mapping between BRAIN entities and CRM IDs.

    Mapping file structure:
    {
        "companies": {
            "Animex": {"crm_id": "cmp_abc", "brain_path": "AREA_Customers/Animex"},
            ...
        },
        "deals": {
            "Animex": {"crm_id": "deal_xyz"},
            ...
        },
        "contacts": {
            "Kamil Kowalski|Animex": {"crm_id": "cnt_123"},
            ...
        }
    }
    """

    def __init__(self, mapping_path: Path):
        self.path = mapping_path
        self._data: dict = {"companies": {}, "deals": {}, "contacts": {}}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            with open(self.path) as f:
                self._data = json.load(f)
        for key in ("companies", "deals", "contacts"):
            self._data.setdefault(key, {})

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    # ─── Company ───

    def get_company_crm_id(self, name: str) -> Optional[str]:
        entry = self._data["companies"].get(name)
        return entry["crm_id"] if entry else None

    def set_company(self, name: str, crm_id: str, brain_path: str = "") -> None:
        self._data["companies"][name] = {"crm_id": crm_id, "brain_path": brain_path}
        self.save()

    def get_company_by_crm_id(self, crm_id: str) -> Optional[str]:
        for name, entry in self._data["companies"].items():
            if entry["crm_id"] == crm_id:
                return name
        return None

    def get_brain_path(self, name: str) -> Optional[str]:
        entry = self._data["companies"].get(name)
        return entry.get("brain_path") if entry else None

    # ─── Deal ───

    def get_deal_crm_id(self, company_name: str) -> Optional[str]:
        entry = self._data["deals"].get(company_name)
        return entry["crm_id"] if entry else None

    def set_deal(self, company_name: str, crm_id: str) -> None:
        self._data["deals"][company_name] = {"crm_id": crm_id}
        self.save()

    def get_deal_company_by_crm_id(self, crm_id: str) -> Optional[str]:
        for name, entry in self._data["deals"].items():
            if entry["crm_id"] == crm_id:
                return name
        return None

    # ─── Contact ───

    def _contact_key(self, name: str, company: str) -> str:
        return f"{name}|{company}"

    def get_contact_crm_id(self, name: str, company: str) -> Optional[str]:
        key = self._contact_key(name, company)
        entry = self._data["contacts"].get(key)
        return entry["crm_id"] if entry else None

    def set_contact(self, name: str, company: str, crm_id: str) -> None:
        key = self._contact_key(name, company)
        self._data["contacts"][key] = {"crm_id": crm_id}
        self.save()
```

- [ ] **Step 2: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/identity.py && git commit -m "feat: identity mapping manager for BRAIN ↔ CRM"
```

---

### Task 11: Build BRAIN → CRM sync engine

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/brain_to_crm.py`

- [ ] **Step 1: Create BRAIN→CRM sync module**

```python
"""BRAIN → CRM sync: parses markdown changes and pushes to CRM API."""

import logging
import subprocess
from pathlib import Path

from brain_parser import (
    extract_sync_section,
    parse_pipeline_table,
    parse_outreach_table,
    parse_profile_yaml,
    parse_meeting_sections,
    parse_reminders,
)
from crm_client import CrmClient
from identity import IdentityMap

log = logging.getLogger("sync.brain_to_crm")

# ─── Stage name → CRM stage mapping (populated at runtime) ───
STAGE_MAP: dict[str, str] = {}  # {"WYGRANA": "stage_id_xxx", ...}

BRAIN_STAGE_TO_CRM = {
    "Nowy": "Nowy",
    "Kontakt": "Kontakt",
    "Discovery": "Discovery",
    "Propozycja": "Propozycja",
    "Negocjacje": "Negocjacje",
    "WYGRANA": "Wygrana",
    "PRZEGRANA": "Przegrana",
    "Odlozona": "Odłożona",
}

SOURCE_MAP = {
    "Ref.": "REFERRAL",
    "LinkedIn": "LINKEDIN",
    "Inbound (dokodu.it)": "WEBSITE_FORM",
    "Istniejący klient": "MANUAL",
    "Przetarg": "MANUAL",
}


def init_stage_map(crm: CrmClient) -> None:
    """Load pipeline stages from CRM into STAGE_MAP."""
    global STAGE_MAP
    stages = crm.list_pipeline_stages()
    STAGE_MAP = {s["name"]: s["id"] for s in stages}
    log.info(f"Loaded {len(STAGE_MAP)} pipeline stages")


def get_changed_files(repo_path: Path, last_sha: str) -> list[str]:
    """Get list of files changed since last_sha."""
    result = subprocess.run(
        ["git", "diff", "--name-only", last_sha, "HEAD"],
        cwd=repo_path, capture_output=True, text=True,
    )
    if result.returncode != 0:
        log.error(f"git diff failed: {result.stderr}")
        return []
    return [f for f in result.stdout.strip().splitlines() if f]


def get_current_sha(repo_path: Path) -> str:
    """Get current HEAD SHA."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path, capture_output=True, text=True,
    )
    return result.stdout.strip()


def sync_pipeline(repo_path: Path, crm: CrmClient, idmap: IdentityMap) -> int:
    """Sync CRM_Leady_B2B.md pipeline table → CRM deals."""
    crm_file = repo_path / "20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md"
    if not crm_file.exists():
        return 0

    content = crm_file.read_text(encoding="utf-8")
    try:
        section = extract_sync_section(content, "PIPELINE")
    except ValueError:
        log.warning("No SYNC:PIPELINE markers found")
        return 0

    rows = parse_pipeline_table(section)
    synced = 0

    for row in rows:
        company_name = row["firma"]
        crm_deal_id = idmap.get_deal_crm_id(company_name)

        stage_name = BRAIN_STAGE_TO_CRM.get(row["etap"], row["etap"])
        stage_id = STAGE_MAP.get(stage_name)
        if not stage_id and row["etap"]:
            log.warning(f"Unknown stage '{row['etap']}' for {company_name} — check BRAIN_STAGE_TO_CRM mapping")

        # Parse value (handle "~20 000", "18 000", "62 000 – 66 000", etc.)
        raw_val = row["wartosc"].replace("~", "").replace(" ", "").split("–")[0].split("-")[0]
        try:
            value = int(raw_val) if raw_val.isdigit() else None
        except (ValueError, TypeError):
            value = None

        deal_data = {
            "title": company_name,
            "value": value,
            "nextStep": row["nastepny_krok"] if row["nastepny_krok"] != "—" else None,
        }
        if stage_id:
            deal_data["stageId"] = stage_id

        if crm_deal_id:
            try:
                crm.update_deal(crm_deal_id, deal_data)
                synced += 1
            except Exception as e:
                log.error(f"Failed to update deal {company_name}: {e}")
        else:
            # Ensure company exists first
            company_crm_id = idmap.get_company_crm_id(company_name)
            if not company_crm_id:
                # Search CRM before creating (avoid duplicates — W3 fix)
                try:
                    results = crm.search(company_name)
                    for r in (results if isinstance(results, list) else results.get("results", [])):
                        if r.get("type") == "company" and company_name.lower() in r.get("name", "").lower():
                            company_crm_id = r["id"]
                            idmap.set_company(company_name, company_crm_id)
                            break
                except Exception:
                    pass
            if not company_crm_id:
                try:
                    source = SOURCE_MAP.get(row["zrodlo"], "MANUAL")
                    comp = crm.create_company({"name": company_name, "source": source})
                    company_crm_id = comp["id"]
                    idmap.set_company(company_name, company_crm_id)
                except Exception as e:
                    log.error(f"Failed to create company {company_name}: {e}")
                    continue

            deal_data["companyId"] = company_crm_id
            try:
                deal = crm.create_deal(deal_data)
                idmap.set_deal(company_name, deal["id"])
                synced += 1
            except Exception as e:
                log.error(f"Failed to create deal {company_name}: {e}")

    log.info(f"Pipeline sync: {synced}/{len(rows)} deals synced")
    return synced


def sync_outreach(repo_path: Path, crm: CrmClient, idmap: IdentityMap) -> int:
    """Sync Outreach_Tracker.md → CRM contacts + activities."""
    outreach_file = repo_path / "20_AREAS/AREA_Marketing_Sales/Outreach_Tracker.md"
    if not outreach_file.exists():
        return 0

    content = outreach_file.read_text(encoding="utf-8")
    try:
        section = extract_sync_section(content, "OUTREACH")
    except ValueError:
        log.warning("No SYNC:OUTREACH markers found")
        return 0

    rows = parse_outreach_table(section)
    synced = 0

    for row in rows:
        company_name = row["firma"]
        person_name = row["osoba"]
        if not person_name:
            continue

        # Ensure company exists
        company_crm_id = idmap.get_company_crm_id(company_name)
        if not company_crm_id:
            try:
                comp = crm.create_company({"name": company_name, "source": "LINKEDIN"})
                company_crm_id = comp["id"]
                idmap.set_company(company_name, company_crm_id)
            except Exception as e:
                log.error(f"Failed to create company {company_name}: {e}")
                continue

        # Create/update contact
        contact_crm_id = idmap.get_contact_crm_id(person_name, company_name)
        names = person_name.split(" ", 1)
        contact_data = {
            "firstName": names[0],
            "lastName": names[1] if len(names) > 1 else "",
            "position": row["stanowisko"],
            "companyId": company_crm_id,
        }

        if not contact_crm_id:
            try:
                contact = crm.create_contact(contact_data)
                idmap.set_contact(person_name, company_name, contact["id"])
                synced += 1
            except Exception as e:
                log.error(f"Failed to create contact {person_name}: {e}")
        else:
            try:
                crm.update_contact(contact_crm_id, contact_data)
                synced += 1
            except Exception as e:
                log.error(f"Failed to update contact {person_name}: {e}")

    log.info(f"Outreach sync: {synced}/{len(rows)} contacts synced")
    return synced


def sync_profiles(repo_path: Path, changed_files: list[str], crm: CrmClient, idmap: IdentityMap) -> int:
    """Sync changed Profile.md files → CRM companies."""
    synced = 0
    for fpath in changed_files:
        if "AREA_Customers" not in fpath or "Profile.md" not in fpath:
            continue

        full_path = repo_path / fpath
        if not full_path.exists():
            continue

        content = full_path.read_text(encoding="utf-8")
        yaml_data = parse_profile_yaml(content)
        crm_id = yaml_data.get("crm_id")

        if crm_id:
            try:
                crm.update_company(crm_id, {
                    "status": yaml_data.get("status", "").upper() or None,
                })
                synced += 1
            except Exception as e:
                log.error(f"Failed to update company from {fpath}: {e}")

    return synced


def sync_meetings(repo_path: Path, changed_files: list[str], crm: CrmClient, idmap: IdentityMap, last_sync_date: str) -> int:
    """Sync new meeting sections from Meetings.md → CRM activities."""
    synced = 0
    for fpath in changed_files:
        if "AREA_Customers" not in fpath or "Meetings.md" not in fpath:
            continue

        full_path = repo_path / fpath
        if not full_path.exists():
            continue

        # Determine company from path: AREA_Customers/Animex/Meetings.md
        parts = Path(fpath).parts
        customer_idx = next((i for i, p in enumerate(parts) if p == "AREA_Customers"), None)
        if customer_idx is None or customer_idx + 1 >= len(parts):
            continue
        company_dir = parts[customer_idx + 1]
        company_crm_id = idmap.get_company_crm_id(company_dir)
        if not company_crm_id:
            log.warning(f"No CRM mapping for company dir: {company_dir}")
            continue

        content = full_path.read_text(encoding="utf-8")
        meetings = parse_meeting_sections(content)

        for m in meetings:
            # Only sync meetings newer than last sync
            if m["date"] <= last_sync_date:
                continue
            try:
                crm.create_activity({
                    "type": "MEETING",
                    "subject": m["title"],
                    "description": m["content"][:2000],
                    "companyId": company_crm_id,
                    "happenedAt": f"{m['date']}T12:00:00Z",
                })
                synced += 1
            except Exception as e:
                log.error(f"Failed to create meeting activity for {company_dir}: {e}")

    return synced


def run_brain_to_crm(repo_path: Path, crm: CrmClient, idmap: IdentityMap, last_sha: str, last_sync_date: str) -> str:
    """Main entry point. Returns new SHA after sync."""
    current_sha = get_current_sha(repo_path)
    if current_sha == last_sha:
        log.debug("No new commits in BRAIN")
        return current_sha

    changed_files = get_changed_files(repo_path, last_sha)
    log.info(f"BRAIN→CRM: {len(changed_files)} files changed since {last_sha[:8]}")

    init_stage_map(crm)

    # Always sync pipeline and outreach (they read full file, not just diff)
    pipeline_files = {"20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md"}
    outreach_files = {"20_AREAS/AREA_Marketing_Sales/Outreach_Tracker.md"}

    if pipeline_files & set(changed_files):
        sync_pipeline(repo_path, crm, idmap)
    if outreach_files & set(changed_files):
        sync_outreach(repo_path, crm, idmap)

    sync_profiles(repo_path, changed_files, crm, idmap)
    sync_meetings(repo_path, changed_files, crm, idmap, last_sync_date)

    # Sync reminders → CRM tasks
    reminders_file = "REMINDERS.md"
    if reminders_file in changed_files:
        sync_reminders(repo_path, crm)

    crm.post_heartbeat("brain_to_crm")
    return current_sha


def sync_reminders(repo_path: Path, crm: CrmClient) -> int:
    """Sync REMINDERS.md → CRM tasks."""
    from brain_parser import parse_reminders

    reminders_path = repo_path / "REMINDERS.md"
    if not reminders_path.exists():
        return 0

    content = reminders_path.read_text(encoding="utf-8")
    items = parse_reminders(content)
    synced = 0

    for item in items:
        try:
            crm.create_task({
                "title": f"[{item['category']}] {item['text']}",
                "dueDate": f"{item['date']}T09:00:00Z",
                "priority": "MEDIUM",
            })
            synced += 1
        except Exception as e:
            log.error(f"Failed to create task from reminder: {e}")

    log.info(f"Reminders sync: {synced}/{len(items)} tasks created")
    return synced
```

- [ ] **Step 2: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/brain_to_crm.py && git commit -m "feat: BRAIN→CRM sync engine"
```

---

### Task 12: Build CRM → BRAIN sync engine

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/crm_to_brain.py`

- [ ] **Step 1: Create CRM→BRAIN sync module**

```python
"""CRM → BRAIN sync: reads change feed and writes to markdown files."""

import logging
import subprocess
from pathlib import Path
from datetime import datetime

from brain_parser import (
    extract_sync_section,
    update_sync_section,
    parse_profile_yaml,
    update_profile_yaml,
    append_meeting_section,
)
from crm_client import CrmClient
from identity import IdentityMap

log = logging.getLogger("sync.crm_to_brain")

# CRM stage name → BRAIN stage name
CRM_STAGE_TO_BRAIN = {
    "Nowy": "Nowy",
    "Kontakt": "Kontakt",
    "Discovery": "Discovery",
    "Propozycja": "Propozycja",
    "Negocjacje": "Negocjacje",
    "Wygrana": "WYGRANA",
    "Przegrana": "PRZEGRANA",
    "Odłożona": "Odlozona",
}


def apply_deal_change(repo_path: Path, change: dict, idmap: IdentityMap) -> list[str]:
    """Apply a deal change from CRM to BRAIN CRM_Leady_B2B.md. Returns list of modified files."""
    crm_file = repo_path / "20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md"
    if not crm_file.exists():
        return []

    company_name = idmap.get_deal_company_by_crm_id(change["entityId"])
    if not company_name:
        log.warning(f"No BRAIN mapping for deal {change['entityId']}")
        return []

    content = crm_file.read_text(encoding="utf-8")
    try:
        section = extract_sync_section(content, "PIPELINE")
    except ValueError:
        return []

    lines = section.strip().splitlines()
    modified = False
    new_lines = []

    for line in lines:
        if f"| {company_name} |" in line or f" {company_name} " in line:
            cells = [c.strip() for c in line.split("|")]
            # cells[0] = "", cells[1] = #, cells[2] = firma, ...
            fields = change.get("fields", {})

            if "stageId" in fields or "stageName" in fields:
                meta = change.get("metadata", {})
                stage_name = meta.get("stageName", fields.get("stageName", ""))
                brain_stage = CRM_STAGE_TO_BRAIN.get(stage_name, stage_name)
                if brain_stage and len(cells) > 5:
                    cells[5] = f" {brain_stage} "
                    modified = True

            if "value" in fields and fields["value"] is not None:
                val = str(fields["value"])
                # Format: "18 000"
                try:
                    formatted = f"{int(float(val)):,}".replace(",", " ")
                except (ValueError, TypeError):
                    formatted = val
                if len(cells) > 6:
                    cells[6] = f" {formatted} "
                    modified = True

            if "nextStep" in fields and fields["nextStep"]:
                if len(cells) > 7:
                    cells[7] = f" {fields['nextStep']} "
                    modified = True

            line = "|".join(cells)

        new_lines.append(line)

    if modified:
        new_section = "\n".join(new_lines)
        content = update_sync_section(content, "PIPELINE", new_section)
        crm_file.write_text(content, encoding="utf-8")
        log.info(f"Updated deal {company_name} in BRAIN pipeline")
        return [str(crm_file.relative_to(repo_path))]

    return []


def apply_activity_change(repo_path: Path, change: dict, idmap: IdentityMap) -> list[str]:
    """Apply a new activity (comment, meeting) from CRM to BRAIN Meetings.md."""
    fields = change.get("fields", {})
    activity_type = fields.get("type", "")
    company_id = fields.get("companyId")

    if not company_id:
        return []

    company_name = idmap.get_company_by_crm_id(company_id)
    if not company_name:
        return []

    brain_path = idmap.get_brain_path(company_name)
    if not brain_path:
        return []

    meetings_file = repo_path / "20_AREAS" / brain_path / "Meetings.md"
    if not meetings_file.exists():
        return []

    content = meetings_file.read_text(encoding="utf-8")
    user = change.get("user", "CRM")
    date = change.get("timestamp", "")[:10]
    subject = fields.get("subject", activity_type)
    description = fields.get("description", "")

    if activity_type == "COMMENT":
        title = f"Komentarz ({user}, {date})"
    else:
        title = f"{activity_type} ({user})"

    body = f"{subject}\n\n{description}" if description else subject

    content = append_meeting_section(content, date, title, body)
    meetings_file.write_text(content, encoding="utf-8")
    log.info(f"Added {activity_type} to {company_name}/Meetings.md")
    return [str(meetings_file.relative_to(repo_path))]


def git_commit_and_push(repo_path: Path, files: list[str], message: str) -> bool:
    """Stage specific files, commit, and push. Returns True on success."""
    if not files:
        return True

    # Stage only modified files
    for f in files:
        subprocess.run(["git", "add", f], cwd=repo_path, capture_output=True)

    # Check if there's anything to commit
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_path, capture_output=True,
    )
    if status.returncode == 0:
        log.debug("No staged changes to commit")
        return True

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo_path, capture_output=True, text=True,
        env={
            **__import__("os").environ,
            "GIT_AUTHOR_NAME": "BRAIN Sync Daemon",
            "GIT_AUTHOR_EMAIL": "sync@dokodu.it",
            "GIT_COMMITTER_NAME": "BRAIN Sync Daemon",
            "GIT_COMMITTER_EMAIL": "sync@dokodu.it",
        },
    )
    if result.returncode != 0:
        log.error(f"git commit failed: {result.stderr}")
        return False

    # Push with rebase
    result = subprocess.run(
        ["git", "pull", "--rebase", "origin", "main"],
        cwd=repo_path, capture_output=True, text=True,
    )
    if result.returncode != 0:
        log.error(f"git pull --rebase failed: {result.stderr}")
        subprocess.run(["git", "rebase", "--abort"], cwd=repo_path, capture_output=True)
        return False

    result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=repo_path, capture_output=True, text=True,
    )
    if result.returncode != 0:
        log.error(f"git push failed: {result.stderr}")
        return False

    log.info(f"Committed and pushed: {message}")
    return True


def run_crm_to_brain(repo_path: Path, crm: CrmClient, idmap: IdentityMap, last_sync_cursor: str) -> str:
    """Main entry point. Returns new sync cursor."""
    changes_resp = crm.get_changes(last_sync_cursor)
    changes = changes_resp.get("changes", [])

    if not changes:
        log.debug("No new CRM changes")
        return last_sync_cursor

    log.info(f"CRM→BRAIN: {len(changes)} changes since {last_sync_cursor}")

    # Pull latest BRAIN
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=repo_path, capture_output=True)

    modified_files = []

    for change in changes:
        entity = change["entity"]
        action = change["action"]

        if entity == "sync":
            continue  # Skip heartbeats

        if entity == "deal":
            modified_files.extend(apply_deal_change(repo_path, change, idmap))
        elif entity == "activity" and action == "create":
            modified_files.extend(apply_activity_change(repo_path, change, idmap))

    # Deduplicate
    modified_files = list(set(modified_files))

    if modified_files:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        git_commit_and_push(
            repo_path, modified_files,
            f"sync: CRM → BRAIN [{timestamp}]"
        )

    crm.post_heartbeat("crm_to_brain")
    return changes_resp.get("syncCursor", last_sync_cursor)
```

- [ ] **Step 2: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/crm_to_brain.py && git commit -m "feat: CRM→BRAIN sync engine"
```

---

### Task 13: Build main daemon runner

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/daemon.py`

- [ ] **Step 1: Create daemon.py**

```python
#!/usr/bin/env python3
"""DOKODU BRAIN ↔ CRM Sync Daemon.

Usage:
  python3 daemon.py                  # Run once (for testing)
  python3 daemon.py --loop           # Run in loop (every 5 min)
  python3 daemon.py --brain-to-crm   # One direction only
  python3 daemon.py --crm-to-brain   # One direction only
  python3 daemon.py --init           # Initial full import BRAIN→CRM
"""

import argparse
import fcntl
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from crm_client import CrmClient
from identity import IdentityMap
from brain_to_crm import run_brain_to_crm, init_stage_map, sync_pipeline, sync_outreach
from crm_to_brain import run_crm_to_brain

log = logging.getLogger("sync")


def setup_logging(log_dir: str) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(f"{log_dir}/sync.log"),
            logging.StreamHandler(),
        ],
    )


class SyncState:
    """Persists sync state between runs."""

    def __init__(self, path: Path):
        self.path = path
        self._data = {
            "last_brain_sha": "",
            "last_crm_cursor": "2020-01-01T00:00:00Z",
            "last_sync_date": "2020-01-01",
            "last_run": None,
        }
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            with open(self.path) as f:
                self._data.update(json.load(f))

    def save(self) -> None:
        self._data["last_run"] = datetime.utcnow().isoformat()
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2)

    @property
    def last_brain_sha(self) -> str:
        return self._data["last_brain_sha"]

    @last_brain_sha.setter
    def last_brain_sha(self, value: str) -> None:
        self._data["last_brain_sha"] = value

    @property
    def last_crm_cursor(self) -> str:
        return self._data["last_crm_cursor"]

    @last_crm_cursor.setter
    def last_crm_cursor(self, value: str) -> None:
        self._data["last_crm_cursor"] = value

    @property
    def last_sync_date(self) -> str:
        return self._data["last_sync_date"]

    @last_sync_date.setter
    def last_sync_date(self, value: str) -> None:
        self._data["last_sync_date"] = value


def acquire_lock(lock_file: str) -> int | None:
    """Try to acquire an exclusive lock. Returns fd on success, None if locked."""
    Path(lock_file).parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_file, os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.write(fd, str(os.getpid()).encode())
        os.ftruncate(fd, len(str(os.getpid())))
        return fd
    except OSError:
        os.close(fd)
        return None


def release_lock(fd: int, lock_file: str) -> None:
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
    try:
        os.unlink(lock_file)
    except OSError:
        pass


def git_pull(repo_path: Path) -> None:
    subprocess.run(
        ["git", "pull", "--rebase", "origin", "main"],
        cwd=repo_path, capture_output=True,
    )


def run_sync(config: dict, direction: str = "both") -> None:
    repo_path = Path(config["brain_repo_path"])
    state_path = repo_path / config["state_file"]
    mapping_path = repo_path / config["mapping_file"]

    crm = CrmClient(config["crm_base_url"], config["crm_api_key"])
    idmap = IdentityMap(mapping_path)
    state = SyncState(state_path)

    # Pull latest BRAIN
    git_pull(repo_path)

    if direction in ("both", "brain_to_crm"):
        new_sha = run_brain_to_crm(
            repo_path, crm, idmap,
            state.last_brain_sha, state.last_sync_date,
        )
        state.last_brain_sha = new_sha

    if direction in ("both", "crm_to_brain"):
        new_cursor = run_crm_to_brain(
            repo_path, crm, idmap,
            state.last_crm_cursor,
        )
        state.last_crm_cursor = new_cursor

    state.last_sync_date = datetime.utcnow().strftime("%Y-%m-%d")
    state.save()
    idmap.save()


def initial_import(config: dict) -> None:
    """Full BRAIN → CRM import (day zero)."""
    repo_path = Path(config["brain_repo_path"])
    mapping_path = repo_path / config["mapping_file"]

    crm = CrmClient(config["crm_base_url"], config["crm_api_key"])
    idmap = IdentityMap(mapping_path)

    init_stage_map(crm)
    sync_pipeline(repo_path, crm, idmap)
    sync_outreach(repo_path, crm, idmap)

    idmap.save()
    log.info("Initial import complete")


def main():
    parser = argparse.ArgumentParser(description="DOKODU BRAIN ↔ CRM Sync Daemon")
    parser.add_argument("--loop", action="store_true", help="Run in continuous loop")
    parser.add_argument("--brain-to-crm", action="store_true", help="Only BRAIN→CRM")
    parser.add_argument("--crm-to-brain", action="store_true", help="Only CRM→BRAIN")
    parser.add_argument("--init", action="store_true", help="Initial full import")
    parser.add_argument("--config", help="Path to config JSON")
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(config["log_dir"])

    if args.init:
        initial_import(config)
        return

    direction = "both"
    if args.brain_to_crm:
        direction = "brain_to_crm"
    elif args.crm_to_brain:
        direction = "crm_to_brain"

    if args.loop:
        log.info(f"Starting sync daemon (interval: {config['sync_interval_seconds']}s)")
        while True:
            lock_fd = acquire_lock(config["lock_file"])
            if lock_fd is None:
                log.warning("Another sync instance is running, skipping")
            else:
                try:
                    run_sync(config, direction)
                except Exception as e:
                    log.exception(f"Sync failed: {e}")
                finally:
                    release_lock(lock_fd, config["lock_file"])

            time.sleep(config["sync_interval_seconds"])
    else:
        lock_fd = acquire_lock(config["lock_file"])
        if lock_fd is None:
            log.error("Another sync instance is running")
            sys.exit(1)
        try:
            run_sync(config, direction)
        finally:
            release_lock(lock_fd, config["lock_file"])


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make executable**

```bash
chmod +x /home/kacper/DOKODU_BRAIN/scripts/sync_daemon/daemon.py
```

- [ ] **Step 3: Test locally (dry run)**

```bash
cd /home/kacper/DOKODU_BRAIN/scripts/sync_daemon && python3 daemon.py --brain-to-crm
```

Expected: Logs showing sync attempt (may fail on CRM connection if running locally — that's OK)

- [ ] **Step 4: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/daemon.py && git commit -m "feat: sync daemon main runner with lock, loop, and init modes"
```

---

## Phase 4: CRM UI Features

### Task 14: Add Outreach Board page to CRM

**Files:**
- Create: `/home/kacper/DOKODU/CRM/src/app/(app)/outreach/page.tsx`
- Create: `/home/kacper/DOKODU/CRM/src/components/outreach/outreach-board.tsx`
- Create: `/home/kacper/DOKODU/CRM/src/components/outreach/outreach-card.tsx`
- Modify: `/home/kacper/DOKODU/CRM/src/components/layout/sidebar.tsx` (add nav link)

This task creates a new "Outreach" page that shows LinkedIn prospecting status. Data comes from Activities with type=LINKEDIN_MESSAGE and Contact metadata synced from Outreach_Tracker.md.

- [ ] **Step 1: Read current sidebar to understand nav pattern**

Read `/home/kacper/DOKODU/CRM/src/components/layout/sidebar.tsx` to see how nav items are structured.

- [ ] **Step 2: Add Outreach nav link to sidebar**

Add a new nav item for "/outreach" with a Users icon (or similar), between Pipeline and Calendar.

- [ ] **Step 3: Create outreach-card.tsx**

A card component showing: contact name, company, position, status badge (zaproszenie/DM/odpowiedz), follow-up date with overdue highlighting (red if past).

- [ ] **Step 4: Create outreach-board.tsx**

A board/table component that:
- Groups contacts by company
- Shows status progression: zaproszenie → zaakceptowane → DM → odpowiedź → call → propozycja
- Highlights overdue follow-ups in red
- Filter: "Do obsługi dziś" (follow-up date = today or past)

Data source: Contacts linked to companies where source=LINKEDIN, with activities showing outreach status.

- [ ] **Step 5: Create page.tsx**

```typescript
// /home/kacper/DOKODU/CRM/src/app/(app)/outreach/page.tsx
import { OutreachBoard } from "@/components/outreach/outreach-board";

export default function OutreachPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">LinkedIn Outreach</h1>
      <OutreachBoard />
    </div>
  );
}
```

- [ ] **Step 6: Test in browser**

Navigate to `system.dokodu.it/outreach` — should show the board (empty until first sync).

- [ ] **Step 7: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/app/\(app\)/outreach/ src/components/outreach/ src/components/layout/sidebar.tsx && git commit -m "feat: Outreach Board page for LinkedIn prospecting"
```

---

### Task 15: Add comments and flags to deals/companies

**Files:**
- Modify: `/home/kacper/DOKODU/CRM/prisma/schema.prisma` (add `flagged` field to Deal and Company)
- Create: `/home/kacper/DOKODU/CRM/src/components/shared/comment-box.tsx`
- Create: `/home/kacper/DOKODU/CRM/src/components/shared/flag-toggle.tsx`
- Modify: `/home/kacper/DOKODU/CRM/src/app/(app)/deals/[id]/deal-detail.tsx` (add comments + flag)
- Modify: `/home/kacper/DOKODU/CRM/src/app/(app)/companies/[id]/company-detail.tsx` (add comments + flag)

- [ ] **Step 1: Add flagged field to schema**

In `prisma/schema.prisma`, add to Deal and Company models:

```prisma
flagged     Boolean  @default(false)
flaggedAt   DateTime?
flaggedBy   String?
```

Push schema: `npx prisma db push && npx prisma generate`

- [ ] **Step 2: Create comment-box.tsx**

A simple form component: textarea + submit button. Creates an Activity with type=NOTE (comment). Shows existing comments (Activities of type NOTE) in reverse chronological order.

- [ ] **Step 3: Create flag-toggle.tsx**

A toggle button: "Wymaga uwagi" — sets `flagged=true` on the entity. Yellow/red badge visible on Kanban cards.

- [ ] **Step 4: Wire into deal-detail.tsx**

Add `<CommentBox dealId={deal.id} />` and `<FlagToggle entity="deal" entityId={deal.id} flagged={deal.flagged} />` to the deal detail page.

- [ ] **Step 5: Wire into company-detail.tsx**

Same pattern for company detail page.

- [ ] **Step 6: Update Kanban card to show flag badge**

In `/home/kacper/DOKODU/CRM/src/components/pipeline/kanban-card.tsx`, add a yellow "!" badge when `deal.flagged === true`.

- [ ] **Step 7: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add prisma/schema.prisma src/components/shared/comment-box.tsx src/components/shared/flag-toggle.tsx src/app/\(app\)/deals/ src/app/\(app\)/companies/ src/components/pipeline/kanban-card.tsx && git commit -m "feat: comments and flags on deals and companies"
```

---

### Task 16: Enhance Dashboard Kanban with pipeline math

**Files:**
- Modify: `/home/kacper/DOKODU/CRM/src/components/pipeline/pipeline-summary.tsx`
- Modify: `/home/kacper/DOKODU/CRM/src/components/pipeline/kanban-column.tsx`

- [ ] **Step 1: Add weighted pipeline calculation**

In `pipeline-summary.tsx`, calculate and display:
- Total open pipeline value (sum of all non-won, non-lost deals)
- Weighted pipeline (sum of value × stage probability for each deal)
- Won this month / this quarter

- [ ] **Step 2: Add per-column totals**

In `kanban-column.tsx`, show sum of deal values at the bottom of each column.

- [ ] **Step 3: Add sync status in footer**

Read from `/api/sync/status` and show "Ostatni sync: X min temu" in the app shell footer. Green dot if healthy, red if >15 min stale.

- [ ] **Step 4: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/components/pipeline/ src/components/layout/ && git commit -m "feat: pipeline math, column totals, sync status indicator"
```

---

### Task 17: Enhance unified timeline

**Files:**
- Modify: `/home/kacper/DOKODU/CRM/src/components/activities/activity-timeline.tsx`
- Modify: `/home/kacper/DOKODU/CRM/src/components/activities/activity-card.tsx`

- [ ] **Step 1: Add source indicator to activity card**

Show who created the activity: "Kacper (via BRAIN)", "Alina (via CRM)", or "Sync Daemon". Use the `user` field from ChangeLog or Activity creator.

- [ ] **Step 2: Add inline comment form**

Below the timeline, add a quick "Dodaj komentarz" form that creates an Activity of type NOTE — which will be synced to BRAIN.

- [ ] **Step 3: Commit**

```bash
cd /home/kacper/DOKODU/CRM && git add src/components/activities/ && git commit -m "feat: enhanced timeline with source indicators and inline comments"
```

---

## Phase 5: Data Cleanup & Deployment

### Task 18: Data cleanup script

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/cleanup.py`

- [ ] **Step 1: Create cleanup script**

```python
#!/usr/bin/env python3
"""One-time data cleanup before first sync. Run manually."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from crm_client import CrmClient

def main():
    config = load_config()
    crm = CrmClient(config["crm_base_url"], config["crm_api_key"])

    # List all deals
    deals = crm.list_deals()
    print(f"Found {len(deals)} deals in CRM:")
    for d in deals:
        company = d.get("company", {}).get("name", "???")
        value = d.get("value", "???")
        print(f"  - {company}: {value} PLN (id: {d['id']})")

    print("\nReview the above. The script will NOT auto-delete.")
    print("To clean up, use CRM UI or MCP tools to fix/remove incorrect entries.")
    print("Then run: python3 daemon.py --init")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run cleanup to audit CRM state**

```bash
cd /home/kacper/DOKODU_BRAIN/scripts/sync_daemon && python3 cleanup.py
```

- [ ] **Step 3: Fix incorrect data via CRM MCP or UI**

Remove/fix: Cichy-Zasada 25k, Corleonis 8900 (use CRM UI or MCP tools).

- [ ] **Step 4: Run initial import**

```bash
python3 daemon.py --init
```

- [ ] **Step 5: Verify in CRM UI**

Check system.dokodu.it — pipeline should match BRAIN CRM_Leady_B2B.md.

- [ ] **Step 6: Commit**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/cleanup.py && git commit -m "feat: data cleanup and initial import script"
```

---

### Task 19: Deploy sync daemon to VPS

**Files:**
- Create: `/home/kacper/DOKODU_BRAIN/scripts/sync_daemon/dokodu-sync.service` (systemd unit)

- [ ] **Step 1: Create systemd service file**

```ini
[Unit]
Description=DOKODU BRAIN ↔ CRM Sync Daemon
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=deploy
WorkingDirectory=/srv/dokodu-brain/scripts/sync_daemon
ExecStart=/usr/bin/python3 /srv/dokodu-brain/scripts/sync_daemon/daemon.py --loop
Restart=always
RestartSec=30
Environment=SYNC_CONFIG=/home/deploy/.config/dokodu/sync_config.json

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 2: Deploy to VPS**

```bash
# Clone BRAIN repo on VPS (if not already)
ssh deploy@57.128.219.9 "git clone git@github.com:Kacpers/DOKODU_BRAIN.git /srv/dokodu-brain || (cd /srv/dokodu-brain && git pull)"

# Install Python deps
ssh deploy@57.128.219.9 "pip3 install requests ruamel.yaml python-dateutil"

# Create config
ssh deploy@57.128.219.9 "mkdir -p ~/.config/dokodu && cat > ~/.config/dokodu/sync_config.json << 'EOF'
{
  \"brain_repo_path\": \"/srv/dokodu-brain\",
  \"crm_base_url\": \"https://system.dokodu.it\",
  \"crm_api_key_file\": \"/home/deploy/.config/dokodu/crm_api_key\",
  \"sync_interval_seconds\": 300,
  \"log_dir\": \"/var/log/dokodu-sync\"
}
EOF"

# Copy API key
ssh deploy@57.128.219.9 "echo 'YOUR_CRM_API_KEY' > ~/.config/dokodu/crm_api_key"

# Install and start service
ssh deploy@57.128.219.9 "sudo cp /srv/dokodu-brain/scripts/sync_daemon/dokodu-sync.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable dokodu-sync && sudo systemctl start dokodu-sync"

# Verify
ssh deploy@57.128.219.9 "sudo systemctl status dokodu-sync"
```

- [ ] **Step 3: Verify logs**

```bash
ssh deploy@57.128.219.9 "tail -20 /var/log/dokodu-sync/sync.log"
```

Expected: "Starting sync daemon (interval: 300s)" + periodic sync logs.

- [ ] **Step 4: Commit service file**

```bash
cd /home/kacper/DOKODU_BRAIN && git add scripts/sync_daemon/dokodu-sync.service && git commit -m "feat: systemd service for sync daemon deployment"
```

---

### Task 20: Auto git pull hook for Claude Code

**Files:**
- Modify: `/home/kacper/.claude/settings.json` (add hook)

- [ ] **Step 1: Add SessionStart hook**

Add to `hooks` in settings.json:

```json
"SessionStart": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "cd /home/kacper/DOKODU_BRAIN && git pull --rebase origin main 2>/dev/null || true"
      }
    ]
  }
]
```

This runs `git pull` at the start of every Claude Code session in DOKODU_BRAIN, ensuring Kacper sees CRM→BRAIN changes from Alina.

- [ ] **Step 2: Test by starting a new session**

Start a new Claude Code session — should see git pull output (or "Already up to date").

- [ ] **Step 3: Commit (in BRAIN for docs)**

```bash
cd /home/kacper/DOKODU_BRAIN && git add docs/ && git commit -m "docs: auto git pull hook for Claude Code sessions"
```

---

## Execution Order & Dependencies

```
Task 1 (ChangeLog model)
  └→ Task 2 (change-log.ts utility)
       └→ Task 3 (wire into API routes)
            └→ Task 4 (/api/changes endpoint)
                 └→ Task 5 (/api/sync/status)

Task 6 (sync markers in BRAIN) — independent

Task 7 (daemon structure) — independent
  └→ Task 8 (brain_parser.py + tests)
       └→ Task 9 (CRM API client)
            └→ Task 10 (identity mapping)
                 └→ Task 11 (BRAIN→CRM engine)
                      └→ Task 12 (CRM→BRAIN engine)
                           └→ Task 13 (daemon runner)

Task 14 (Outreach Board UI) — after Task 3
Task 15 (Comments + Flags) — after Task 3
Task 16 (Dashboard Kanban) — after Task 5
Task 17 (Timeline) — after Task 3

Task 18 (Data cleanup) — after Tasks 11-13
  └→ Task 19 (Deploy daemon)
       └→ Task 20 (Auto git pull hook)
```

**Parallelizable groups:**
- Tasks 1-5 (CRM backend) can run in parallel with Tasks 6-13 (BRAIN + daemon)
- Tasks 14-17 (CRM UI) can run in parallel with each other, after Task 3
- Tasks 18-20 are sequential (deploy phase)
