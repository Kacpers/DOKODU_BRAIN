# Dokodu CRM — Phase 1 (Foundation MVP) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully functional, deployable CRM at `crm.dokodu.it` with RBAC, company/contact management, deal pipeline with Kanban board, activity timeline, attachments, audit log, GDPR compliance, global search, and a basic dashboard.

**Architecture:** Next.js 15 App Router with Server Components for data fetching, Prisma ORM with PostgreSQL, NextAuth for JWT-based auth with invite-only registration, shadcn/ui component library. All API routes protected by RBAC middleware with scope-based data isolation. Soft deletes on core entities.

**Tech Stack:** Next.js 15, TypeScript, Prisma 6, PostgreSQL 16, NextAuth 5, shadcn/ui, Tailwind CSS 3, Lucide React, DnD Kit, Zod (validation), bcryptjs

**Spec:** `docs/superpowers/specs/2026-03-29-dokodu-crm-design.md`
**Repo:** `https://github.com/Kacpers/Dokodu-crm`
**Local path:** `~/DOKODU/CRM`

---

## File Structure

```
~/DOKODU/CRM/
├── prisma/
│   ├── schema.prisma              # Full data model
│   └── seed.ts                    # Default pipeline, roles, permissions, admin user
├── src/
│   ├── app/
│   │   ├── layout.tsx             # Root layout with sidebar nav
│   │   ├── page.tsx               # Dashboard (redirect to /dashboard)
│   │   ├── globals.css            # Tailwind globals
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx     # Login page
│   │   │   ├── register/page.tsx  # Invite-based registration
│   │   │   └── layout.tsx         # Auth layout (no sidebar)
│   │   ├── (app)/
│   │   │   ├── layout.tsx         # App layout with sidebar + topbar
│   │   │   ├── dashboard/page.tsx # KPI cards + tasks + recent activity
│   │   │   ├── companies/
│   │   │   │   ├── page.tsx       # Company list (DataTable)
│   │   │   │   ├── new/page.tsx   # Create company form
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx   # Company detail (tabs)
│   │   │   │       └── edit/page.tsx
│   │   │   ├── contacts/
│   │   │   │   ├── page.tsx       # Contact list
│   │   │   │   └── [id]/page.tsx  # Contact detail
│   │   │   ├── pipeline/page.tsx  # Kanban board
│   │   │   ├── deals/
│   │   │   │   ├── page.tsx       # Deal list
│   │   │   │   ├── new/page.tsx   # Create deal
│   │   │   │   └── [id]/page.tsx  # Deal detail (timeline + sidebar)
│   │   │   ├── settings/
│   │   │   │   ├── page.tsx       # Settings overview
│   │   │   │   ├── pipeline/page.tsx  # Pipeline stage config
│   │   │   │   ├── users/page.tsx     # User management + invite
│   │   │   │   └── roles/page.tsx     # Role + permission matrix
│   │   │   └── search/page.tsx    # Full search results page
│   │   └── api/
│   │       ├── auth/[...nextauth]/route.ts
│   │       ├── auth/invite/route.ts
│   │       ├── auth/register/route.ts
│   │       ├── companies/route.ts         # GET (list), POST (create)
│   │       ├── companies/[id]/route.ts    # GET, PATCH, DELETE
│   │       ├── contacts/route.ts
│   │       ├── contacts/[id]/route.ts
│   │       ├── deals/route.ts
│   │       ├── deals/[id]/route.ts
│   │       ├── deals/[id]/stage/route.ts  # PATCH stage change
│   │       ├── deals/[id]/contacts/route.ts # manage DealContacts
│   │       ├── deals/pipeline/route.ts    # GET kanban data
│   │       ├── activities/route.ts
│   │       ├── attachments/route.ts       # POST upload
│   │       ├── attachments/[id]/route.ts  # GET download, DELETE
│   │       ├── search/route.ts            # GET global search
│   │       ├── tags/route.ts
│   │       ├── tags/[id]/route.ts
│   │       ├── audit-log/route.ts
│   │       ├── gdpr/export/[contactId]/route.ts
│   │       ├── gdpr/anonymize/[contactId]/route.ts
│   │       ├── pipelines/route.ts
│   │       ├── pipelines/[id]/stages/route.ts
│   │       ├── roles/route.ts
│   │       ├── roles/[id]/permissions/route.ts
│   │       └── users/route.ts
│   ├── lib/
│   │   ├── prisma.ts              # Prisma client singleton + soft delete middleware
│   │   ├── auth.ts                # NextAuth config (credentials provider)
│   │   ├── auth-helpers.ts        # getSession, requireAuth, requirePermission
│   │   ├── rbac.ts                # Permission checking logic + scope filtering
│   │   ├── audit.ts               # Audit log helper (logAction)
│   │   ├── search.ts              # Full-text search query builder
│   │   ├── validation/
│   │   │   ├── company.ts         # Zod schemas for company
│   │   │   ├── contact.ts
│   │   │   ├── deal.ts
│   │   │   ├── activity.ts
│   │   │   └── pipeline.ts
│   │   └── utils.ts               # Shared utilities (pagination, error response)
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components (auto-generated)
│   │   ├── layout/
│   │   │   ├── sidebar.tsx        # Left sidebar navigation
│   │   │   ├── topbar.tsx         # Top bar with search + user menu
│   │   │   └── command-menu.tsx   # Cmd+K global search
│   │   ├── companies/
│   │   │   ├── company-table.tsx  # DataTable for company list
│   │   │   ├── company-form.tsx   # Create/edit company form
│   │   │   └── company-tabs.tsx   # Detail page tabs
│   │   ├── contacts/
│   │   │   ├── contact-table.tsx
│   │   │   └── contact-form.tsx
│   │   ├── deals/
│   │   │   ├── deal-table.tsx
│   │   │   ├── deal-form.tsx
│   │   │   ├── deal-detail.tsx    # Two-column layout
│   │   │   └── deal-sidebar.tsx   # Right sidebar with deal info
│   │   ├── pipeline/
│   │   │   ├── kanban-board.tsx   # DnD Kit board
│   │   │   ├── kanban-column.tsx  # Stage column
│   │   │   ├── kanban-card.tsx    # Deal card
│   │   │   └── pipeline-summary.tsx # Weighted value footer
│   │   ├── activities/
│   │   │   ├── activity-timeline.tsx  # Chronological list
│   │   │   ├── activity-form.tsx      # Quick add (note, call, email, meeting)
│   │   │   └── activity-card.tsx      # Single activity in timeline
│   │   ├── dashboard/
│   │   │   ├── kpi-cards.tsx
│   │   │   ├── recent-activities.tsx
│   │   │   └── sla-alerts.tsx
│   │   └── shared/
│   │       ├── data-table.tsx     # Reusable DataTable (shadcn)
│   │       ├── pagination.tsx
│   │       ├── tag-badge.tsx
│   │       ├── icp-badge.tsx
│   │       ├── status-badge.tsx
│   │       ├── file-upload.tsx
│   │       └── confirm-dialog.tsx
│   └── types/
│       └── index.ts               # Shared TypeScript types
├── public/
│   └── uploads/                   # Local file storage (Phase 1)
├── .env.example
├── .env.local
├── package.json
├── tsconfig.json
├── next.config.ts
├── tailwind.config.ts
├── postcss.config.js
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
├── docker-compose.dev.yml
└── CLAUDE.md                      # Instructions for Claude Code working in this repo
```

---

## Task 1: Project Scaffolding & Database Setup

**Files:**
- Create: `package.json`, `tsconfig.json`, `next.config.ts`, `tailwind.config.ts`, `postcss.config.js`, `.env.example`, `.env.local`, `.gitignore`, `CLAUDE.md`
- Create: `src/app/layout.tsx`, `src/app/globals.css`, `src/app/page.tsx`
- Create: `docker-compose.dev.yml` (PostgreSQL for dev)

- [ ] **Step 1: Clone repo and initialize Next.js project**

```bash
cd ~/DOKODU
git clone https://github.com/Kacpers/Dokodu-crm.git CRM
cd CRM
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --turbopack
```

If repo already has files, init Next.js in a temp dir and copy over.

- [ ] **Step 2: Install core dependencies**

```bash
pnpm add prisma @prisma/client next-auth@beta @auth/prisma-adapter bcryptjs zod
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select @radix-ui/react-tabs @radix-ui/react-label @radix-ui/react-switch @radix-ui/react-tooltip
pnpm add lucide-react class-variance-authority clsx tailwind-merge
pnpm add -D @types/bcryptjs prisma
```

- [ ] **Step 3: Initialize shadcn/ui**

```bash
npx shadcn@latest init
```

Select: New York style, Slate base color, CSS variables.

Then add components:

```bash
npx shadcn@latest add button input label card table dialog sheet select tabs badge command dropdown-menu separator avatar tooltip textarea checkbox popover calendar
```

- [ ] **Step 4: Create docker-compose.dev.yml for PostgreSQL**

```yaml
# docker-compose.dev.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: dokodu_crm
      POSTGRES_USER: crm
      POSTGRES_PASSWORD: crm_dev_password
    ports:
      - "5433:5432"  # 5433 to avoid conflict with dokodu.it DB
    volumes:
      - crm_pgdata:/var/lib/postgresql/data

volumes:
  crm_pgdata:
```

- [ ] **Step 5: Create .env.example and .env.local**

```env
# .env.example
DATABASE_URL="postgresql://crm:crm_dev_password@localhost:5433/dokodu_crm"
NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"
NEXTAUTH_URL="http://localhost:3001"

# Admin seed credentials
ADMIN_EMAIL="kacper@dokodu.it"
ADMIN_PASSWORD="change-me-immediately"
```

Copy to `.env.local` with real values.

- [ ] **Step 6: Create CLAUDE.md**

```markdown
# CLAUDE.md — Dokodu CRM

## What is this
Standalone CRM for Dokodu agency. Manages B2B sales lifecycle.

## Tech stack
Next.js 15 (App Router), TypeScript, Prisma, PostgreSQL, NextAuth, shadcn/ui, Tailwind CSS

## Commands
- `pnpm dev` — start dev server (port 3001)
- `pnpm build` — production build
- `npx prisma db push` — push schema changes
- `npx prisma db seed` — seed default data
- `npx prisma studio` — open DB GUI

## Conventions
- API routes in `src/app/api/` — all protected by `requirePermission()` middleware
- Validation with Zod schemas in `src/lib/validation/`
- Audit log on all CRUD operations via `logAction()` from `src/lib/audit.ts`
- Soft deletes on Company, ContactPerson, Deal (filter `deletedAt IS NULL`)
- Pagination: offset-based, `?page=1&pageSize=25`
- Error format: `{ error: { code: "...", message: "...", details?: [...] } }`

## Design spec
`~/DOKODU_BRAIN/docs/superpowers/specs/2026-03-29-dokodu-crm-design.md`
```

- [ ] **Step 7: Update next.config.ts for port 3001**

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // CRM runs on port 3001 (dokodu.it uses 3000)
};

export default nextConfig;
```

Add to `package.json` scripts: `"dev": "next dev -p 3001"`

- [ ] **Step 8: Start PostgreSQL and verify**

```bash
docker compose -f docker-compose.dev.yml up -d
```

Run: `docker compose -f docker-compose.dev.yml ps`
Expected: postgres container running on port 5433

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "feat: initialize Next.js project with Prisma, shadcn/ui, PostgreSQL

- Next.js 15 with App Router and TypeScript
- shadcn/ui component library configured
- PostgreSQL 16 via Docker Compose (port 5433)
- CLAUDE.md with project conventions"
```

---

## Task 2: Prisma Schema — Full Data Model

**Files:**
- Create: `prisma/schema.prisma`
- Create: `src/lib/prisma.ts`

- [ ] **Step 1: Create Prisma schema**

Write the full schema from the spec. This is the largest single file. Include ALL models from the spec:

Core: `User`, `Role`, `Permission`, `RolePermission`, `UserRole`, `InviteToken`
Business: `Company`, `ContactPerson`, `Deal`, `DealContact`, `DealStageHistory`, `DealValueHistory`
Pipeline: `Pipeline`, `PipelineStage`
Activity: `Activity`, `Attachment`, `AuditLog`
Tags: `Tag`, `TagOnCompany`, `TagOnDeal`
System: `SystemSetting`, `ApiKey`, `WebhookEvent`, `Notification`
Project (stub): `Project`, `Milestone`, `Invoice` (models defined but UI comes in Phase 2)

All enums from the spec. All indexes. All relations including reverse relations.

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ==================== AUTH & RBAC ====================

model User {
  id                  String   @id @default(cuid())
  name                String
  email               String   @unique
  passwordHash        String
  avatarUrl           String?
  isActive            Boolean  @default(true)
  lastLoginAt         DateTime?
  failedLoginAttempts Int      @default(0)
  lockedUntil         DateTime?

  roles              UserRole[]
  assignedDeals      Deal[]           @relation("assignedDeals")
  assignedTasks      Task[]           @relation("assignedTasks")
  createdTasks       Task[]           @relation("createdTasks")
  activities         Activity[]
  timeLogs           TimeLog[]
  calendarEvents     CalendarEvent[]
  gmailConnection    GmailConnection?
  stageChanges       DealStageHistory[]
  imports            LeadImport[]
  apiKeys            ApiKey[]
  auditLogs          AuditLog[]
  notifications      Notification[]
  uploadedAttachments Attachment[]     @relation("uploadedAttachments")
  dealValueChanges   DealValueHistory[]
  defaultPipelines   Pipeline[]       @relation("defaultPipeline")
  assignedCompanies  Company[]
  assignedProjects   Project[]

  createdAt          DateTime @default(now())
  updatedAt          DateTime @updatedAt
}

model Role {
  id          String   @id @default(cuid())
  name        String   @unique
  description String?
  isSystem    Boolean  @default(false)
  permissions RolePermission[]
  users       UserRole[]
}

model Permission {
  id          String   @id @default(cuid())
  code        String   @unique
  group       String
  description String
  roles       RolePermission[]
}

model RolePermission {
  roleId       String
  permissionId String
  scope        PermissionScope @default(ALL)
  role         Role       @relation(fields: [roleId], references: [id])
  permission   Permission @relation(fields: [permissionId], references: [id])
  @@id([roleId, permissionId])
}

enum PermissionScope { OWN ALL }

model UserRole {
  userId String
  roleId String
  user   User @relation(fields: [userId], references: [id])
  role   Role @relation(fields: [roleId], references: [id])
  @@id([userId, roleId])
}

model InviteToken {
  id        String   @id @default(cuid())
  email     String
  token     String   @unique
  roleId    String
  expiresAt DateTime
  usedAt    DateTime?
  createdAt DateTime @default(now())
}

// ==================== BUSINESS ENTITIES ====================
// ... (continue with ALL models from spec)
```

The full schema is 400+ lines. Copy ALL models exactly as defined in the spec, including:
- All enums (CompanySize, CompanyStatus, IcpScore, LeadSource, ContactRole, StageType, ServiceType, DealType, LostReasonCategory, ActivityType, TaskPriority, TaskStatus, TaskType, CalendarEventType, ProjectStatus, MilestoneStatus, InvoiceStatus, InvoiceSource, ImportSource, ImportStatus, WebhookSource, WebhookStatus, NotificationType, ConsentType, EmailDirection, PermissionScope)
- All @@index and @@unique constraints
- All relation fields on both sides

- [ ] **Step 2: Create Prisma client singleton with soft delete middleware**

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query"] : [],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

// Soft delete middleware — auto-filter deletedAt IS NULL
prisma.$use(async (params, next) => {
  const softDeleteModels = ["Company", "ContactPerson", "Deal"];

  if (softDeleteModels.includes(params.model ?? "")) {
    if (params.action === "findMany" || params.action === "findFirst") {
      if (!params.args) params.args = {};
      if (!params.args.where) params.args.where = {};
      if (params.args.where.deletedAt === undefined) {
        params.args.where.deletedAt = null;
      }
    }

    if (params.action === "delete") {
      params.action = "update";
      params.args.data = { deletedAt: new Date() };
    }

    if (params.action === "deleteMany") {
      params.action = "updateMany";
      if (!params.args) params.args = {};
      params.args.data = { deletedAt: new Date() };
    }
  }

  return next(params);
});
```

- [ ] **Step 3: Push schema to database**

```bash
npx prisma db push
```

Expected: "Your database is now in sync with your Prisma schema."

- [ ] **Step 4: Verify with Prisma Studio**

```bash
npx prisma studio
```

Expected: Opens browser with all tables visible, empty.

- [ ] **Step 5: Commit**

```bash
git add prisma/schema.prisma src/lib/prisma.ts
git commit -m "feat: add complete Prisma schema with all CRM models

- 30+ models covering RBAC, companies, contacts, deals, pipeline,
  activities, projects, invoices, audit log, GDPR
- Soft delete middleware for core entities
- All indexes and unique constraints"
```

---

## Task 3: Seed Data — Roles, Permissions, Pipeline, Admin User

**Files:**
- Create: `prisma/seed.ts`
- Modify: `package.json` (add prisma seed config)

- [ ] **Step 1: Create seed script**

```typescript
// prisma/seed.ts
import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

const PERMISSIONS = [
  // Companies
  { code: "companies:create", group: "companies", description: "Create companies" },
  { code: "companies:read", group: "companies", description: "Read companies" },
  { code: "companies:update", group: "companies", description: "Update companies" },
  { code: "companies:delete", group: "companies", description: "Delete companies" },
  { code: "companies:assign", group: "companies", description: "Assign companies to users" },
  // Contacts
  { code: "contacts:create", group: "contacts", description: "Create contacts" },
  { code: "contacts:read", group: "contacts", description: "Read contacts" },
  { code: "contacts:update", group: "contacts", description: "Update contacts" },
  { code: "contacts:delete", group: "contacts", description: "Delete contacts" },
  // Deals
  { code: "deals:create", group: "deals", description: "Create deals" },
  { code: "deals:read", group: "deals", description: "Read deals" },
  { code: "deals:update", group: "deals", description: "Update deals" },
  { code: "deals:delete", group: "deals", description: "Delete deals" },
  // Activities
  { code: "activities:create", group: "activities", description: "Create activities" },
  { code: "activities:read", group: "activities", description: "Read activities" },
  // Tasks
  { code: "tasks:create", group: "tasks", description: "Create tasks" },
  { code: "tasks:read", group: "tasks", description: "Read tasks" },
  { code: "tasks:update", group: "tasks", description: "Update tasks" },
  // Time logs
  { code: "timelogs:create", group: "timelogs", description: "Create time logs" },
  { code: "timelogs:read", group: "timelogs", description: "Read time logs" },
  // Projects
  { code: "projects:create", group: "projects", description: "Create projects" },
  { code: "projects:read", group: "projects", description: "Read projects" },
  { code: "projects:update", group: "projects", description: "Update projects" },
  // Invoices
  { code: "invoices:create", group: "invoices", description: "Create invoices" },
  { code: "invoices:read", group: "invoices", description: "Read invoices" },
  { code: "invoices:update", group: "invoices", description: "Update invoices" },
  // Analytics
  { code: "analytics:view", group: "analytics", description: "View analytics" },
  // Pipeline
  { code: "pipeline:configure", group: "pipeline", description: "Configure pipeline stages" },
  // Settings
  { code: "settings:manage", group: "settings", description: "Manage system settings" },
  { code: "users:manage", group: "users", description: "Manage users and roles" },
  // Import/Export
  { code: "import:csv", group: "import", description: "Import CSV data" },
  { code: "export:data", group: "export", description: "Export data" },
];

// Scope: OWN = see only own records, ALL = see everything
const ROLE_PERMISSIONS: Record<string, Record<string, "OWN" | "ALL">> = {
  Admin: Object.fromEntries(PERMISSIONS.map((p) => [p.code, "ALL"])),
  Sales: {
    "companies:create": "OWN", "companies:read": "OWN", "companies:update": "OWN",
    "contacts:create": "ALL", "contacts:read": "ALL", "contacts:update": "ALL",
    "deals:create": "OWN", "deals:read": "OWN", "deals:update": "OWN",
    "activities:create": "OWN", "activities:read": "OWN",
    "tasks:create": "OWN", "tasks:read": "OWN", "tasks:update": "OWN",
    "timelogs:create": "OWN", "timelogs:read": "OWN",
    "projects:create": "OWN", "projects:read": "OWN", "projects:update": "OWN",
    "invoices:read": "OWN",
    "analytics:view": "OWN",
    "import:csv": "ALL",
  },
  Viewer: {
    "companies:read": "ALL", "contacts:read": "ALL", "deals:read": "ALL",
    "activities:read": "ALL", "projects:read": "ALL", "invoices:read": "ALL",
    "analytics:view": "ALL", "timelogs:create": "OWN", "timelogs:read": "OWN",
  },
};

const PIPELINE_STAGES = [
  { name: "Nowy Lead", position: 1, color: "#94a3b8", type: "OPEN", probability: 5, slaDays: 2 },
  { name: "Kontakt", position: 2, color: "#3b82f6", type: "OPEN", probability: 10, slaDays: 3 },
  { name: "Discovery Call", position: 3, color: "#8b5cf6", type: "OPEN", probability: 25, slaDays: 5 },
  { name: "Propozycja", position: 4, color: "#f97316", type: "OPEN", probability: 50, slaDays: 5 },
  { name: "Negocjacje", position: 5, color: "#eab308", type: "OPEN", probability: 75, slaDays: 7 },
  { name: "Wygrana", position: 6, color: "#22c55e", type: "WON", probability: 100, slaDays: null },
  { name: "Przegrana", position: 7, color: "#ef4444", type: "LOST", probability: 0, slaDays: null },
  { name: "Odlozona", position: 8, color: "#64748b", type: "DEFERRED", probability: 0, slaDays: null },
];

async function main() {
  console.log("Seeding permissions...");
  for (const perm of PERMISSIONS) {
    await prisma.permission.upsert({
      where: { code: perm.code },
      update: {},
      create: perm,
    });
  }

  console.log("Seeding roles...");
  for (const [roleName, perms] of Object.entries(ROLE_PERMISSIONS)) {
    const role = await prisma.role.upsert({
      where: { name: roleName },
      update: {},
      create: { name: roleName, description: `${roleName} role`, isSystem: true },
    });

    for (const [permCode, scope] of Object.entries(perms)) {
      const permission = await prisma.permission.findUnique({ where: { code: permCode } });
      if (permission) {
        await prisma.rolePermission.upsert({
          where: { roleId_permissionId: { roleId: role.id, permissionId: permission.id } },
          update: { scope },
          create: { roleId: role.id, permissionId: permission.id, scope },
        });
      }
    }
  }

  console.log("Seeding default pipeline...");
  const pipeline = await prisma.pipeline.upsert({
    where: { id: "default-pipeline" },
    update: {},
    create: { id: "default-pipeline", name: "Sprzedaz B2B", isDefault: true },
  });

  for (const stage of PIPELINE_STAGES) {
    await prisma.pipelineStage.upsert({
      where: { pipelineId_position: { pipelineId: pipeline.id, position: stage.position } },
      update: stage,
      create: { ...stage, pipelineId: pipeline.id } as any,
    });
  }

  console.log("Seeding admin user...");
  const adminRole = await prisma.role.findUnique({ where: { name: "Admin" } });
  const passwordHash = await bcrypt.hash(process.env.ADMIN_PASSWORD || "admin123", 12);

  const admin = await prisma.user.upsert({
    where: { email: process.env.ADMIN_EMAIL || "kacper@dokodu.it" },
    update: {},
    create: {
      name: "Kacper Sieradzinski",
      email: process.env.ADMIN_EMAIL || "kacper@dokodu.it",
      passwordHash,
    },
  });

  if (adminRole) {
    await prisma.userRole.upsert({
      where: { userId_roleId: { userId: admin.id, roleId: adminRole.id } },
      update: {},
      create: { userId: admin.id, roleId: adminRole.id },
    });
  }

  console.log("Seed complete.");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
```

- [ ] **Step 2: Add seed config to package.json**

Add to `package.json`:
```json
{
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
  }
}
```

Install ts-node: `pnpm add -D ts-node`

- [ ] **Step 3: Run seed**

```bash
npx prisma db seed
```

Expected: "Seeding permissions... Seeding roles... Seeding default pipeline... Seeding admin user... Seed complete."

- [ ] **Step 4: Verify in Prisma Studio**

```bash
npx prisma studio
```

Check: 3 roles, 30+ permissions, 8 pipeline stages, 1 admin user with Admin role.

- [ ] **Step 5: Commit**

```bash
git add prisma/seed.ts package.json pnpm-lock.yaml
git commit -m "feat: add seed script with roles, permissions, pipeline, admin user

- 30 permissions across 12 resource groups
- 3 default roles (Admin/Sales/Viewer) with scoped permissions
- B2B pipeline with 8 stages (from Sales Playbook)
- Admin user seeded from env vars"
```

---

## Task 4: Authentication — NextAuth + Login + Invite Registration

**Files:**
- Create: `src/lib/auth.ts`, `src/lib/auth-helpers.ts`
- Create: `src/app/api/auth/[...nextauth]/route.ts`
- Create: `src/app/api/auth/invite/route.ts`, `src/app/api/auth/register/route.ts`
- Create: `src/app/(auth)/layout.tsx`, `src/app/(auth)/login/page.tsx`, `src/app/(auth)/register/page.tsx`
- Create: `src/middleware.ts`

- [ ] **Step 1: Create NextAuth configuration**

```typescript
// src/lib/auth.ts
import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";
import { prisma } from "./prisma";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
          include: {
            roles: {
              include: {
                role: {
                  include: {
                    permissions: {
                      include: { permission: true },
                    },
                  },
                },
              },
            },
          },
        });

        if (!user || !user.isActive) return null;

        // Check lock
        if (user.lockedUntil && user.lockedUntil > new Date()) return null;

        const valid = await bcrypt.compare(credentials.password as string, user.passwordHash);

        if (!valid) {
          // Increment failed attempts
          const attempts = user.failedLoginAttempts + 1;
          await prisma.user.update({
            where: { id: user.id },
            data: {
              failedLoginAttempts: attempts,
              lockedUntil: attempts >= 5 ? new Date(Date.now() + 15 * 60 * 1000) : null,
            },
          });
          return null;
        }

        // Reset on success
        await prisma.user.update({
          where: { id: user.id },
          data: { failedLoginAttempts: 0, lockedUntil: null, lastLoginAt: new Date() },
        });

        // Flatten permissions
        const permissions = user.roles.flatMap((ur) =>
          ur.role.permissions.map((rp) => ({
            code: rp.permission.code,
            scope: rp.scope,
          }))
        );

        return {
          id: user.id,
          name: user.name,
          email: user.email,
          permissions,
        };
      },
    }),
  ],
  session: { strategy: "jwt", maxAge: 24 * 60 * 60 },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.permissions = (user as any).permissions;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        (session.user as any).permissions = token.permissions;
      }
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
});
```

- [ ] **Step 2: Create auth helpers (requireAuth, requirePermission)**

```typescript
// src/lib/auth-helpers.ts
import { auth } from "./auth";
import { NextResponse } from "next/server";

type PermissionEntry = { code: string; scope: "OWN" | "ALL" };

export async function getServerSession() {
  return await auth();
}

export async function requireAuth() {
  const session = await auth();
  if (!session?.user) {
    throw new Error("UNAUTHENTICATED");
  }
  return session.user as { id: string; name: string; email: string; permissions: PermissionEntry[] };
}

export function hasPermission(
  permissions: PermissionEntry[],
  code: string
): { allowed: boolean; scope: "OWN" | "ALL" | null } {
  const perm = permissions.find((p) => p.code === code);
  if (!perm) return { allowed: false, scope: null };
  return { allowed: true, scope: perm.scope };
}

export async function requirePermission(permissionCode: string) {
  const user = await requireAuth();
  const check = hasPermission(user.permissions, permissionCode);
  if (!check.allowed) {
    throw new Error("FORBIDDEN");
  }
  return { user, scope: check.scope! };
}

export function errorResponse(error: unknown) {
  if (error instanceof Error) {
    if (error.message === "UNAUTHENTICATED") {
      return NextResponse.json({ error: { code: "UNAUTHENTICATED", message: "Not authenticated" } }, { status: 401 });
    }
    if (error.message === "FORBIDDEN") {
      return NextResponse.json({ error: { code: "FORBIDDEN", message: "Insufficient permissions" } }, { status: 403 });
    }
  }
  console.error(error);
  return NextResponse.json({ error: { code: "INTERNAL_ERROR", message: "Internal server error" } }, { status: 500 });
}
```

- [ ] **Step 3: Create NextAuth route handler**

```typescript
// src/app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/lib/auth";
export const { GET, POST } = handlers;
```

- [ ] **Step 4: Create middleware for route protection**

```typescript
// src/middleware.ts
export { auth as middleware } from "@/lib/auth";

export const config = {
  matcher: [
    "/((?!login|register|api/auth|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

- [ ] **Step 5: Create login page**

```typescript
// src/app/(auth)/layout.tsx
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      {children}
    </div>
  );
}
```

```typescript
// src/app/(auth)/login/page.tsx
"use client";

import { signIn } from "next-auth/react";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const result = await signIn("credentials", {
      email,
      password,
      redirect: false,
    });

    if (result?.error) {
      setError("Nieprawidlowy email lub haslo");
      setLoading(false);
    } else {
      router.push("/dashboard");
    }
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-2xl font-semibold text-center">Dokodu CRM</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Haslo</Label>
            <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          {error && <p className="text-sm text-red-500">{error}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Logowanie..." : "Zaloguj sie"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 6: Create invite API endpoint**

```typescript
// src/app/api/auth/invite/route.ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requirePermission, errorResponse } from "@/lib/auth-helpers";
import { randomBytes } from "crypto";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  roleId: z.string(),
});

export async function POST(req: NextRequest) {
  try {
    await requirePermission("users:manage");
    const body = await req.json();
    const { email, roleId } = schema.parse(body);

    const token = randomBytes(32).toString("hex");
    const invite = await prisma.inviteToken.create({
      data: {
        email,
        token,
        roleId,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      },
    });

    const inviteUrl = `${process.env.NEXTAUTH_URL}/register?token=${token}`;

    return NextResponse.json({ inviteUrl, expiresAt: invite.expiresAt });
  } catch (error) {
    return errorResponse(error);
  }
}
```

- [ ] **Step 7: Create register page and API**

```typescript
// src/app/api/auth/register/route.ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import bcrypt from "bcryptjs";
import { z } from "zod";

const schema = z.object({
  token: z.string(),
  name: z.string().min(2),
  password: z.string().min(8),
});

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { token, name, password } = schema.parse(body);

    const invite = await prisma.inviteToken.findUnique({ where: { token } });
    if (!invite || invite.usedAt || invite.expiresAt < new Date()) {
      return NextResponse.json(
        { error: { code: "INVALID_TOKEN", message: "Invalid or expired invite" } },
        { status: 400 }
      );
    }

    const passwordHash = await bcrypt.hash(password, 12);
    const user = await prisma.user.create({
      data: { name, email: invite.email, passwordHash },
    });

    await prisma.userRole.create({
      data: { userId: user.id, roleId: invite.roleId },
    });

    await prisma.inviteToken.update({
      where: { id: invite.id },
      data: { usedAt: new Date() },
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: { code: "REGISTRATION_FAILED", message: "Registration failed" } },
      { status: 500 }
    );
  }
}
```

Create register page (similar to login, with token from URL query, name + password fields).

- [ ] **Step 8: Verify login flow**

```bash
pnpm dev
```

Navigate to `http://localhost:3001/login`, enter admin credentials from seed. Should redirect to `/dashboard` (which will be a placeholder page for now).

- [ ] **Step 9: Commit**

```bash
git add src/lib/auth.ts src/lib/auth-helpers.ts src/app/api/auth/ src/app/\(auth\)/ src/middleware.ts
git commit -m "feat: add authentication with NextAuth, RBAC helpers, invite registration

- Credentials provider with failed attempt locking (5 attempts = 15 min)
- JWT sessions with permissions embedded in token
- requirePermission() middleware with scope support
- Invite-only registration flow
- Login page UI"
```

---

## Task 5: RBAC Middleware & Scope Filtering

**Files:**
- Create: `src/lib/rbac.ts`
- Create: `src/lib/utils.ts`

- [ ] **Step 1: Create RBAC scope filtering utility**

```typescript
// src/lib/rbac.ts
import { Prisma } from "@prisma/client";

type ScopeContext = {
  userId: string;
  scope: "OWN" | "ALL";
};

/**
 * Returns a Prisma WHERE clause that enforces scope-based filtering.
 * For OWN scope, adds `assignedToId = userId` (or `userId` for activities/timelogs).
 */
export function scopeFilter(
  model: "company" | "deal" | "activity" | "task" | "timeLog" | "project",
  ctx: ScopeContext
): Record<string, unknown> {
  if (ctx.scope === "ALL") return {};

  const scopeField: Record<string, string> = {
    company: "assignedToId",
    deal: "assignedToId",
    activity: "userId",
    task: "assignedToId",
    timeLog: "userId",
    project: "assignedToId",
  };

  return { [scopeField[model]]: ctx.userId };
}

/**
 * Pagination helper — extracts page/pageSize from URL params, returns skip/take.
 */
export function paginationParams(searchParams: URLSearchParams) {
  const page = Math.max(1, parseInt(searchParams.get("page") || "1", 10));
  const pageSize = Math.min(100, Math.max(1, parseInt(searchParams.get("pageSize") || "25", 10)));
  return { skip: (page - 1) * pageSize, take: pageSize, page, pageSize };
}

/**
 * Wraps paginated data in standard response envelope.
 */
export function paginatedResponse<T>(data: T[], total: number, page: number, pageSize: number) {
  return {
    data,
    meta: { total, page, pageSize, totalPages: Math.ceil(total / pageSize) },
  };
}
```

- [ ] **Step 2: Create shared utils**

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

- [ ] **Step 3: Commit**

```bash
git add src/lib/rbac.ts src/lib/utils.ts
git commit -m "feat: add RBAC scope filtering and pagination utilities"
```

---

## Task 6: Audit Log Helper

**Files:**
- Create: `src/lib/audit.ts`

- [ ] **Step 1: Create audit log helper**

```typescript
// src/lib/audit.ts
import { prisma } from "./prisma";

export async function logAction(params: {
  userId: string;
  action: "create" | "update" | "delete" | "export" | "login" | "logout";
  entity: string;
  entityId: string;
  changes?: Record<string, { old: unknown; new: unknown }>;
  ipAddress?: string;
}) {
  await prisma.auditLog.create({
    data: {
      userId: params.userId,
      action: params.action,
      entity: params.entity,
      entityId: params.entityId,
      changes: params.changes ?? undefined,
      ipAddress: params.ipAddress,
    },
  });
}
```

- [ ] **Step 2: Commit**

```bash
git add src/lib/audit.ts
git commit -m "feat: add audit log helper for tracking all data changes"
```

---

## Task 7: Validation Schemas (Zod)

**Files:**
- Create: `src/lib/validation/company.ts`, `contact.ts`, `deal.ts`, `activity.ts`, `pipeline.ts`

- [ ] **Step 1: Create all Zod schemas**

One file per entity. Example for company:

```typescript
// src/lib/validation/company.ts
import { z } from "zod";

export const createCompanySchema = z.object({
  name: z.string().min(1, "Nazwa firmy jest wymagana"),
  nip: z.string().optional(),
  industry: z.string().optional(),
  size: z.enum(["MICRO", "SMALL", "MEDIUM", "LARGE"]).optional(),
  website: z.string().url().optional().or(z.literal("")),
  linkedinUrl: z.string().url().optional().or(z.literal("")),
  city: z.string().optional(),
  icpScore: z.enum(["A", "B", "C", "X"]).optional(),
  source: z.enum(["WEBSITE_FORM", "PRACUJ", "LINKEDIN", "REFERRAL", "CONFERENCE", "COLD_CALL", "BUSINESS_CARD", "MANUAL", "OTHER"]),
  consentType: z.enum(["FORM_SUBMISSION", "LEGITIMATE_INTEREST", "CONTRACT", "MANUAL_CONSENT"]).optional(),
  preferredChannel: z.string().optional(),
  bestContactTime: z.string().optional(),
});

export const updateCompanySchema = createCompanySchema.partial();
```

Create similar schemas for: contact, deal (with dealType, isRecurring fields), activity, pipeline stage config.

- [ ] **Step 2: Commit**

```bash
git add src/lib/validation/
git commit -m "feat: add Zod validation schemas for all CRM entities"
```

---

## Task 8: Company API Routes (CRUD)

**Files:**
- Create: `src/app/api/companies/route.ts` (GET list, POST create)
- Create: `src/app/api/companies/[id]/route.ts` (GET, PATCH, DELETE)

- [ ] **Step 1: Create companies list + create endpoint**

```typescript
// src/app/api/companies/route.ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requirePermission, errorResponse } from "@/lib/auth-helpers";
import { scopeFilter, paginationParams, paginatedResponse } from "@/lib/rbac";
import { createCompanySchema } from "@/lib/validation/company";
import { logAction } from "@/lib/audit";

export async function GET(req: NextRequest) {
  try {
    const { user, scope } = await requirePermission("companies:read");
    const params = req.nextUrl.searchParams;
    const { skip, take, page, pageSize } = paginationParams(params);
    const filter = scopeFilter("company", { userId: user.id, scope });

    // Optional filters
    const where: any = { ...filter };
    if (params.get("status")) where.status = params.get("status");
    if (params.get("icpScore")) where.icpScore = params.get("icpScore");
    if (params.get("source")) where.source = params.get("source");
    if (params.get("assignedToId")) where.assignedToId = params.get("assignedToId");
    if (params.get("search")) {
      where.OR = [
        { name: { contains: params.get("search"), mode: "insensitive" } },
        { nip: { contains: params.get("search") } },
        { city: { contains: params.get("search"), mode: "insensitive" } },
      ];
    }

    const [companies, total] = await Promise.all([
      prisma.company.findMany({
        where,
        skip,
        take,
        orderBy: { updatedAt: "desc" },
        include: {
          assignedTo: { select: { id: true, name: true } },
          _count: { select: { deals: true, contacts: true } },
        },
      }),
      prisma.company.count({ where }),
    ]);

    return NextResponse.json(paginatedResponse(companies, total, page, pageSize));
  } catch (error) {
    return errorResponse(error);
  }
}

export async function POST(req: NextRequest) {
  try {
    const { user } = await requirePermission("companies:create");
    const body = await req.json();
    const data = createCompanySchema.parse(body);

    const company = await prisma.company.create({
      data: { ...data, assignedToId: user.id },
    });

    await logAction({
      userId: user.id,
      action: "create",
      entity: "Company",
      entityId: company.id,
    });

    return NextResponse.json(company, { status: 201 });
  } catch (error) {
    return errorResponse(error);
  }
}
```

- [ ] **Step 2: Create company detail + update + delete endpoint**

```typescript
// src/app/api/companies/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requirePermission, errorResponse } from "@/lib/auth-helpers";
import { scopeFilter } from "@/lib/rbac";
import { updateCompanySchema } from "@/lib/validation/company";
import { logAction } from "@/lib/audit";

export async function GET(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const { user, scope } = await requirePermission("companies:read");
    const filter = scopeFilter("company", { userId: user.id, scope });

    const company = await prisma.company.findFirst({
      where: { id, ...filter },
      include: {
        contacts: true,
        deals: { include: { stage: true } },
        assignedTo: { select: { id: true, name: true } },
        tags: { include: { tag: true } },
      },
    });

    if (!company) {
      return NextResponse.json({ error: { code: "NOT_FOUND", message: "Company not found" } }, { status: 404 });
    }

    return NextResponse.json(company);
  } catch (error) {
    return errorResponse(error);
  }
}

export async function PATCH(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const { user, scope } = await requirePermission("companies:update");
    const filter = scopeFilter("company", { userId: user.id, scope });

    const existing = await prisma.company.findFirst({ where: { id, ...filter } });
    if (!existing) {
      return NextResponse.json({ error: { code: "NOT_FOUND", message: "Company not found" } }, { status: 404 });
    }

    const body = await req.json();
    const data = updateCompanySchema.parse(body);

    // Track changes for audit
    const changes: Record<string, { old: unknown; new: unknown }> = {};
    for (const [key, value] of Object.entries(data)) {
      if ((existing as any)[key] !== value) {
        changes[key] = { old: (existing as any)[key], new: value };
      }
    }

    const company = await prisma.company.update({ where: { id }, data });

    if (Object.keys(changes).length > 0) {
      await logAction({ userId: user.id, action: "update", entity: "Company", entityId: id, changes });
    }

    return NextResponse.json(company);
  } catch (error) {
    return errorResponse(error);
  }
}

export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const { user } = await requirePermission("companies:delete");

    await prisma.company.delete({ where: { id } }); // soft delete via middleware
    await logAction({ userId: user.id, action: "delete", entity: "Company", entityId: id });

    return NextResponse.json({ success: true });
  } catch (error) {
    return errorResponse(error);
  }
}
```

- [ ] **Step 3: Verify with curl**

```bash
# Login and get session cookie
curl -X POST http://localhost:3001/api/auth/callback/credentials \
  -H "Content-Type: application/json" \
  -d '{"email":"kacper@dokodu.it","password":"admin123"}' -c cookies.txt

# Create company
curl -X POST http://localhost:3001/api/companies \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name":"Test Firma","source":"MANUAL"}'

# List companies
curl http://localhost:3001/api/companies -b cookies.txt
```

- [ ] **Step 4: Commit**

```bash
git add src/app/api/companies/
git commit -m "feat: add Company CRUD API with RBAC scope filtering and audit logging"
```

---

## Task 9: Contact, Deal, Activity, Tag API Routes

**Files:** Same pattern as Task 8 for each entity.

- [ ] **Step 1: Create Contact CRUD** (`src/app/api/contacts/route.ts`, `[id]/route.ts`)

Follow the same pattern. Contacts inherit scope from parent Company (join on Company.assignedToId).

- [ ] **Step 2: Create Deal CRUD** (`src/app/api/deals/route.ts`, `[id]/route.ts`)

Deals include: stage change endpoint (`deals/[id]/stage/route.ts`) that:
1. Updates deal stage
2. Creates DealStageHistory record (compute durationInStageHours)
3. Auto-updates Company status (CONTACT→LEAD on first deal, LEAD→CLIENT on won)
4. Returns updated deal

- [ ] **Step 3: Create Deal pipeline endpoint** (`src/app/api/deals/pipeline/route.ts`)

Returns deals grouped by stage for the Kanban board:
```json
{
  "stages": [
    { "id": "...", "name": "Nowy Lead", "color": "#94a3b8", "deals": [...] },
    ...
  ],
  "summary": { "totalValue": 150000, "weightedValue": 45000 }
}
```

- [ ] **Step 4: Create Deal contacts endpoint** (`src/app/api/deals/[id]/contacts/route.ts`)

Manages many-to-many DealContact pivot: POST to add, DELETE to remove, with role assignment.

- [ ] **Step 5: Create Activity API** (`src/app/api/activities/route.ts`)

GET: filterable by dealId, companyId, contactPersonId, userId, type, date range.
POST: create activity + audit log.

- [ ] **Step 6: Create Tag API** (`src/app/api/tags/route.ts`, `[id]/route.ts`)

CRUD for tags + endpoints to assign/remove tags from companies and deals.

- [ ] **Step 7: Create Attachment API** (`src/app/api/attachments/route.ts`, `[id]/route.ts`)

POST: multipart form upload → save to `public/uploads/` with UUID filename. Store metadata in Attachment table.
GET: stream file for download.
DELETE: remove file + record.

- [ ] **Step 8: Create Search API** (`src/app/api/search/route.ts`)

PostgreSQL full-text search across Company.name, ContactPerson name/email, Deal.title. Results grouped by type, scope-filtered, max 5 per type.

- [ ] **Step 9: Create Audit Log API** (`src/app/api/audit-log/route.ts`)

GET: admin only, paginated, filterable by entity, userId, date range.

- [ ] **Step 10: Create GDPR endpoints** (`src/app/api/gdpr/export/[contactId]/route.ts`, `anonymize/[contactId]/route.ts`)

Export: returns all PII for a contact as JSON (admin only).
Anonymize: replaces name/email/phone with "ANONYMIZED", preserves deal values + stage history.

- [ ] **Step 11: Create Pipeline Settings API** (`src/app/api/pipelines/route.ts`, `[id]/stages/route.ts`)

GET/POST pipelines. PATCH stages with reorder support.

- [ ] **Step 12: Create Roles API** (`src/app/api/roles/route.ts`, `[id]/permissions/route.ts`)

CRUD roles. Permission matrix update (set permission+scope per role).

- [ ] **Step 13: Create Users API** (`src/app/api/users/route.ts`)

GET: list users (admin). PATCH: update user (deactivate). Invite flow handled by auth/invite.

- [ ] **Step 14: Commit each group separately**

One commit per entity group (contacts, deals, activities, tags, attachments, search, audit, gdpr, settings).

---

## Task 10: App Layout — Sidebar + Topbar

**Files:**
- Create: `src/app/(app)/layout.tsx`
- Create: `src/components/layout/sidebar.tsx`, `topbar.tsx`, `command-menu.tsx`

- [ ] **Step 1: Create sidebar navigation**

```typescript
// src/components/layout/sidebar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard, Building2, Users, Kanban, HandCoins,
  FolderKanban, FileText, Calendar, CheckSquare, Clock,
  BarChart3, Upload, Settings,
} from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Firmy", href: "/companies", icon: Building2 },
  { name: "Osoby", href: "/contacts", icon: Users },
  { name: "Pipeline", href: "/pipeline", icon: Kanban },
  { name: "Deale", href: "/deals", icon: HandCoins },
  { name: "Projekty", href: "/projects", icon: FolderKanban },
  { name: "Faktury", href: "/invoices", icon: FileText },
  { name: "Kalendarz", href: "/calendar", icon: Calendar },
  { name: "Zadania", href: "/tasks", icon: CheckSquare },
  { name: "Czas pracy", href: "/timelogs", icon: Clock },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Import", href: "/import", icon: Upload },
  { name: "Ustawienia", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-60 flex-col border-r bg-white">
      <div className="flex h-14 items-center border-b px-4">
        <span className="text-lg font-semibold text-slate-900">Dokodu CRM</span>
      </div>
      <nav className="flex-1 space-y-1 p-2">
        {navigation.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                active
                  ? "bg-slate-100 text-slate-900 font-medium"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
```

- [ ] **Step 2: Create topbar with search and user menu**

```typescript
// src/components/layout/topbar.tsx
"use client";

import { useSession, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Search, LogOut } from "lucide-react";

export function Topbar({ onSearchClick }: { onSearchClick: () => void }) {
  const { data: session } = useSession();

  return (
    <header className="flex h-14 items-center justify-between border-b bg-white px-6">
      <Button variant="outline" size="sm" className="gap-2 text-slate-500" onClick={onSearchClick}>
        <Search className="h-4 w-4" />
        <span>Szukaj...</span>
        <kbd className="ml-2 rounded bg-slate-100 px-1.5 py-0.5 text-xs">⌘K</kbd>
      </Button>
      <div className="flex items-center gap-3">
        <span className="text-sm text-slate-600">{session?.user?.name}</span>
        <Button variant="ghost" size="icon" onClick={() => signOut()}>
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
```

- [ ] **Step 3: Create Cmd+K command menu**

Using shadcn `Command` component. Fetches from `/api/search` with debounce. Shows results grouped by type. Click navigates to detail page.

- [ ] **Step 4: Create app layout**

```typescript
// src/app/(app)/layout.tsx
import { SessionProvider } from "next-auth/react";
import { Sidebar } from "@/components/layout/sidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <div className="flex h-screen bg-slate-50">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </SessionProvider>
  );
}
```

- [ ] **Step 5: Verify layout renders**

Navigate to `http://localhost:3001/dashboard` — should show sidebar + empty main area.

- [ ] **Step 6: Commit**

```bash
git add src/app/\(app\)/layout.tsx src/components/layout/
git commit -m "feat: add app layout with sidebar navigation, topbar, and Cmd+K search"
```

---

## Task 11: Company List + Detail Pages

**Files:**
- Create: `src/app/(app)/companies/page.tsx`, `new/page.tsx`, `[id]/page.tsx`
- Create: `src/components/companies/company-table.tsx`, `company-form.tsx`, `company-tabs.tsx`
- Create: `src/components/shared/data-table.tsx`, `status-badge.tsx`, `icp-badge.tsx`

- [ ] **Step 1: Create reusable DataTable component** (shadcn DataTable pattern with sorting, filtering, pagination)
- [ ] **Step 2: Create company list page** with DataTable — columns: name, industry, ICP badge, deal count, status badge, assignee, last contact
- [ ] **Step 3: Create company form** (create/edit) with all fields from Zod schema
- [ ] **Step 4: Create company detail page** with tabs: Osoby, Deale, Aktywnosci, Zadania, Pliki + right sidebar (ICP, tags, source, dates)
- [ ] **Step 5: Create status/ICP badge components** (color-coded)
- [ ] **Step 6: Verify** — create a company, see it in list, click to detail
- [ ] **Step 7: Commit**

---

## Task 12: Contact List + Detail Pages

Same pattern as Task 11, but for ContactPerson. Contact detail shows: company link, deals (via DealContact), activities, role badge.

- [ ] **Step 1-5: Create contact pages and components**
- [ ] **Step 6: Commit**

---

## Task 13: Pipeline Kanban Board

**Files:**
- Create: `src/app/(app)/pipeline/page.tsx`
- Create: `src/components/pipeline/kanban-board.tsx`, `kanban-column.tsx`, `kanban-card.tsx`, `pipeline-summary.tsx`

- [ ] **Step 1: Install DnD Kit**

```bash
pnpm add @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

- [ ] **Step 2: Create Kanban board** — fetches from `/api/deals/pipeline`, renders columns per stage
- [ ] **Step 3: Create Kanban card** — title, company, value, days on stage (red if > SLA), assignee avatar
- [ ] **Step 4: Implement drag-and-drop** — dropping card on new column calls `PATCH /api/deals/:id/stage`
- [ ] **Step 5: Add Won/Lost confirmation dialog** — when dropping on Wygrana/Przegrana, show modal asking for lost reason (if lost) or won date
- [ ] **Step 6: Create pipeline summary footer** — weighted value per stage
- [ ] **Step 7: Add filters** — assignee, service type, value range
- [ ] **Step 8: Verify** — create deals, drag between stages, confirm pipeline updates
- [ ] **Step 9: Commit**

---

## Task 14: Deal List + Detail Pages

**Files:**
- Create: `src/app/(app)/deals/page.tsx`, `new/page.tsx`, `[id]/page.tsx`
- Create: `src/components/deals/deal-table.tsx`, `deal-form.tsx`, `deal-detail.tsx`, `deal-sidebar.tsx`

- [ ] **Step 1: Create deal list** — DataTable with columns: title, company, stage badge, value, assignee, expected close, days on stage
- [ ] **Step 2: Create deal form** — linked to company (searchable select), contact selection, pipeline/stage, value, serviceType, dealType, expectedCloseDate
- [ ] **Step 3: Create deal detail** — two-column layout:
  - Left: Activity timeline with quick-add bar (+Note, +Call, +Email, +Meeting)
  - Right: sidebar with stage, company link, contacts with roles, assignee, service type, value, tags, dates
- [ ] **Step 4: Stage change from detail** — dropdown changes stage, creates DealStageHistory
- [ ] **Step 5: Manage deal contacts** — add/remove contacts with role selection
- [ ] **Step 6: Verify** — create deal from company page, see in pipeline, change stage, add activities
- [ ] **Step 7: Commit**

---

## Task 15: Activity Timeline Component

**Files:**
- Create: `src/components/activities/activity-timeline.tsx`, `activity-form.tsx`, `activity-card.tsx`

- [ ] **Step 1: Create activity card** — icon per type (phone for CALL, mail for EMAIL, etc.), subject, description, who, when, duration
- [ ] **Step 2: Create activity timeline** — chronological list, loads from API with infinite scroll or pagination
- [ ] **Step 3: Create quick-add form** — type selector (Note, Call, Email, Meeting), subject, description, duration, happenedAt
- [ ] **Step 4: Integrate in deal detail and company detail pages**
- [ ] **Step 5: Commit**

---

## Task 16: Dashboard

**Files:**
- Create: `src/app/(app)/dashboard/page.tsx`
- Create: `src/components/dashboard/kpi-cards.tsx`, `recent-activities.tsx`, `sla-alerts.tsx`

- [ ] **Step 1: Create KPI cards** — pipeline value (weighted), deals this month (won/lost/open), overdue tasks count, upcoming meetings
- [ ] **Step 2: Create recent activities feed** — last 10 activities across all deals
- [ ] **Step 3: Create SLA alerts** — deals exceeding stage SLA days (red highlight)
- [ ] **Step 4: Compose dashboard page** — KPI row + 2-column layout (activities left, SLA alerts right)
- [ ] **Step 5: Verify** — dashboard shows real data from created companies/deals
- [ ] **Step 6: Commit**

---

## Task 17: Settings — Pipeline Config, Users, Roles

**Files:**
- Create: `src/app/(app)/settings/page.tsx`, `pipeline/page.tsx`, `users/page.tsx`, `roles/page.tsx`

- [ ] **Step 1: Create pipeline settings page** — list stages, drag to reorder, edit name/color/probability/SLA, add new stage, delete stage
- [ ] **Step 2: Create users page** — list all users with role badges. Invite button → form (email + role select) → calls `/api/auth/invite` → shows invite URL
- [ ] **Step 3: Create roles page** — list roles, click to edit → permission checkbox matrix (grouped by resource)
- [ ] **Step 4: Verify** — change pipeline stage order, invite a user, modify role permissions
- [ ] **Step 5: Commit**

---

## Task 18: Data Migration Script

**Files:**
- Create: `scripts/migrate-brain-data.ts`

- [ ] **Step 1: Write migration script**

Reads from:
1. `DOKODU_BRAIN/20_AREAS/AREA_Customers/*/` — creates Company + ContactPerson records
2. `DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/Lead_Qualification_Full_2026-03-29.md` — creates Company records with ICP scores (status: CONTACT)

Parses markdown files, deduplicates by company name, creates records via Prisma. Creates Activity (type: NOTE) with "Imported from BRAIN" for each imported record.

- [ ] **Step 2: Run migration in dry-run mode**

```bash
npx ts-node scripts/migrate-brain-data.ts --dry-run
```

Expected: prints what would be created without touching DB.

- [ ] **Step 3: Run migration**

```bash
npx ts-node scripts/migrate-brain-data.ts
```

- [ ] **Step 4: Verify in CRM** — companies list shows imported data
- [ ] **Step 5: Commit**

---

## Task 19: Docker Production Setup

**Files:**
- Create: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

- [ ] **Step 1: Create production Dockerfile**

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN npx prisma generate
RUN pnpm build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
COPY --from=builder /app/prisma ./prisma
EXPOSE 3001
CMD ["node", "server.js"]
```

- [ ] **Step 2: Create docker-compose.yml**

```yaml
services:
  crm:
    build: .
    ports:
      - "3001:3001"
    environment:
      DATABASE_URL: "postgresql://crm:${DB_PASSWORD}@db:5432/dokodu_crm"
      NEXTAUTH_SECRET: "${NEXTAUTH_SECRET}"
      NEXTAUTH_URL: "https://crm.dokodu.it"
    depends_on:
      - db
    volumes:
      - uploads:/app/public/uploads

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: dokodu_crm
      POSTGRES_USER: crm
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
  uploads:
```

- [ ] **Step 3: Add next.config.ts standalone output**

```typescript
const nextConfig: NextConfig = {
  output: "standalone",
};
```

- [ ] **Step 4: Build and test locally**

```bash
docker compose build
docker compose up -d
```

- [ ] **Step 5: Commit**

```bash
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "feat: add Docker production setup for crm.dokodu.it deployment"
```

---

## Task 20: Final Integration Test & Polish

- [ ] **Step 1: End-to-end walkthrough**

1. Login as admin
2. Create company (status: CONTACT)
3. Add contact person
4. Create deal → company auto-changes to LEAD
5. See deal on Kanban board
6. Drag deal through stages (Kontakt → Discovery → Propozycja)
7. Add activities (note, call log)
8. Move deal to Wygrana → company auto-changes to CLIENT
9. Check dashboard KPIs update
10. Check audit log in settings

- [ ] **Step 2: Invite a test user with Sales role**

Generate invite link, register as Sales user, verify scope isolation (can only see assigned records).

- [ ] **Step 3: Test Cmd+K search** — search for company, contact, deal by name

- [ ] **Step 4: Fix any issues found**

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "feat: complete Phase 1 MVP — CRM with RBAC, pipeline, contacts, dashboard

Phase 1 delivers:
- RBAC with scope-based data isolation (Admin/Sales/Viewer)
- Company & contact management with status flow
- Deal pipeline with Kanban board (drag-and-drop)
- Activity timeline with quick-add
- Attachments, audit log, GDPR compliance
- Global search (Cmd+K)
- Dashboard with KPIs and SLA alerts
- Invite-only registration
- Docker production setup
- Data migration from BRAIN"
```

---

## Summary

| Task | Description | Est. Complexity |
|------|-------------|:---:|
| 1 | Project scaffolding | Low |
| 2 | Prisma schema (full) | High |
| 3 | Seed data | Medium |
| 4 | Authentication (NextAuth + invite) | High |
| 5 | RBAC middleware + scope filtering | Medium |
| 6 | Audit log helper | Low |
| 7 | Zod validation schemas | Medium |
| 8 | Company API (CRUD) | Medium |
| 9 | Contact, Deal, Activity, Tag, Search, GDPR APIs | High |
| 10 | App layout (sidebar + topbar + Cmd+K) | Medium |
| 11 | Company list + detail pages | High |
| 12 | Contact pages | Medium |
| 13 | Pipeline Kanban board | High |
| 14 | Deal list + detail pages | High |
| 15 | Activity timeline component | Medium |
| 16 | Dashboard | Medium |
| 17 | Settings (pipeline, users, roles) | Medium |
| 18 | Data migration script | Medium |
| 19 | Docker production setup | Low |
| 20 | Integration test & polish | Medium |
