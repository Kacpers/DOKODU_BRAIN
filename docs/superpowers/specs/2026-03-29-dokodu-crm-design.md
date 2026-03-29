# Dokodu CRM — Design Specification

**Date:** 2026-03-29
**Status:** Approved
**Author:** Kacper + Claude

---

## 1. Overview

Standalone CRM system for Dokodu — an AI integration boutique agency. Manages the full client lifecycle: from lead capture through discovery, proposal, negotiation, project delivery, to retainer and upsell.

**Problem:** Lead data scattered across markdown files (BRAIN), CSV exports (Pracuj.pl), LinkedIn, business cards, and phone calls. Pipeline management is 100% manual. No follow-up automation, no interaction history, no analytics.

**Solution:** Dedicated CRM application at `crm.dokodu.it` — separate from the main website (`dokodu.it`) — with pipeline management, activity tracking, task automation, time logging, Gmail sync, calendar integration, and analytics.

---

## 2. Architecture & Stack

**Project:** `dokodu-crm` (separate repo, separate deploy)

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 15+ (App Router, Server Components) |
| Language | TypeScript |
| ORM | Prisma |
| Database | PostgreSQL (separate instance from dokodu.it) |
| Auth | NextAuth (credentials + invite-based registration) |
| UI | shadcn/ui + Tailwind CSS |
| Icons | Lucide React |
| Charts | Chart.js |
| DnD | DnD Kit (Kanban board) |
| Calendar UI | Custom weekly/monthly view |
| Email | Gmail API (read-only sync) |
| Deploy | Docker on same server as dokodu.it, subdomain `crm.dokodu.it` |

### Data Flow

```
dokodu.it form submit → webhook POST → crm.dokodu.it/api/webhooks/dokodu → Lead created
Stripe payment         → webhook POST → crm.dokodu.it/api/webhooks/stripe → Deal updated
Gmail                  → Gmail API poll → emails matched to contacts → Activity timeline
Google Calendar        → two-way sync → CalendarEvent in CRM
Claude Code scripts    → GET /api/external/* → read CRM data (API key auth)
```

### Separation from dokodu.it

- CRM has its own database — no shared tables
- dokodu.it pushes leads via webhook (fire-and-forget)
- Stripe webhooks go to both systems independently
- Shared: same server (Docker), same Google Workspace

---

## 3. RBAC System

Granular role-based access control. Roles are configurable — not hardcoded.

### Models

```
Role { id, name, description, isSystem (bool) }
Permission { id, code, group, description }
RolePermission { roleId, permissionId, scope (OWN | ALL) }
UserRole { userId, roleId }
```

### Permission Codes

Format: `resource:action`. Resources: leads, deals, contacts, companies, activities, tasks, timelogs, analytics, pipeline, users, settings, import, export.

Actions: create, read, update, delete, assign, configure.

### Data Scoping

The `scope` field on `RolePermission` determines data visibility:
- `ALL` — can see/act on all records of this resource
- `OWN` — can only see/act on records where `assignedToId = currentUser` (or `userId` for activities/timelogs)

Scoping rules per resource:
- **Companies, Deals** — scoped by `assignedToId`
- **Activities, TimeLogs** — scoped by `userId`
- **Tasks** — scoped by `assignedToId`
- **Contacts** — scoped through parent Company's `assignedToId`

Middleware signature: `requirePermission('deals:update')` — checks both permission existence AND scope, applying WHERE clause automatically.

### Default Roles (seeded)

| Permission | Admin | Sales | Viewer |
|------------|:-----:|:-----:|:------:|
| companies:create | yes | yes | no |
| companies:read | all | own | all |
| companies:update | yes | own | no |
| companies:delete | yes | no | no |
| companies:assign | yes | no | no |
| deals:create | yes | yes | no |
| deals:read | all | own | all |
| deals:update | yes | own | no |
| deals:delete | yes | no | no |
| contacts:create | yes | yes | no |
| contacts:read | all | all | all |
| contacts:update | yes | yes | no |
| companies:* | yes | yes (no delete) | read |
| activities:create | yes | yes | no |
| activities:read | all | own | all |
| tasks:create | yes | yes | no |
| tasks:read | all | own | no |
| timelogs:read | all | own | own |
| timelogs:create | yes | yes | yes |
| analytics:view | yes | own | yes |
| projects:create | yes | yes | no |
| projects:read | all | own | all |
| projects:update | yes | own | no |
| invoices:create | yes | no | no |
| invoices:read | all | own | all |
| invoices:update | yes | no | no |
| pipeline:configure | yes | no | no |
| settings:manage | yes | no | no |
| users:manage | yes | no | no |
| import:csv | yes | yes | no |
| export:data | yes | no | no |

**Data scoping:** Sales role sees only records assigned to them (where `assignedToId = currentUser`), unless granted `read_all`.

**Enforcement:**
- API middleware: `requirePermission('deals:update')` on every route
- Server Components: conditional rendering based on user permissions (no delete button without `deals:delete`)
- Admin can create custom roles via UI (checkbox matrix of permissions)

**Registration:** Invite-only. Admin generates invite link → recipient registers with credentials.

---

## 4. Data Model

### Companies & Contacts

```prisma
model Company {
  id              String   @id @default(cuid())
  name            String
  nip             String?  @unique
  industry        String?
  size            CompanySize?
  website         String?
  linkedinUrl     String?
  city            String?
  itStack         Json?    // { erp: "SAP", email: "O365", aiAdoption: "basic" }
  icpScore        IcpScore?
  icpFitReasons   Json?    // checklist results from ICP
  status          CompanyStatus @default(CONTACT)
  source          LeadSource
  consentType     ConsentType?  // RODO: basis for data processing
  consentDate     DateTime?
  assignedToId    String?
  assignedTo      User?    @relation(fields: [assignedToId], references: [id])
  contacts        ContactPerson[]
  deals           Deal[]
  activities      Activity[]
  tasks           Task[]
  timeLogs        TimeLog[]
  tags            TagOnCompany[]
  emailThreads    EmailThread[]
  attachments     Attachment[]
  projects        Project[]
  invoices        Invoice[]
  calendarEvents  CalendarEvent[]
  npsScore        Int?         // last NPS (1-10)
  npsUpdatedAt    DateTime?
  trustLevel      Int?         // 1-5 (relationship quality)
  preferredChannel String?     // "Email", "Phone", "Teams", "LinkedIn"
  bestContactTime  String?     // "Mon-Fri 10-12"
  deletedAt       DateTime?  // soft delete
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  @@index([assignedToId])
  @@index([icpScore])
}

enum CompanySize { MICRO SMALL MEDIUM LARGE }
enum CompanyStatus { CONTACT PROSPECT LEAD CLIENT FORMER_CLIENT }
enum IcpScore { A B C X }
enum LeadSource { WEBSITE_FORM PRACUJ LINKEDIN REFERRAL CONFERENCE COLD_CALL BUSINESS_CARD MANUAL OTHER }

model ContactPerson {
  id           String   @id @default(cuid())
  firstName    String
  lastName     String
  email        String?
  phone        String?
  position     String?
  roleType     ContactRole?
  companyId    String
  company      Company  @relation(fields: [companyId], references: [id])
  linkedinUrl  String?
  isPrimary    Boolean  @default(false)
  notes        String?
  dealContacts DealContact[]  // many-to-many with deals
  activities   Activity[]
  tasks        Task[]
  calendarEvents CalendarEvent[]
  emailThreads EmailThread[]
  deletedAt    DateTime?  // soft delete
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt

  @@index([companyId])
  @@index([email])
}

enum ContactRole { DECISION_MAKER CHAMPION USER BLOCKER INFLUENCER }
```

### Pipeline & Deals

```prisma
model Pipeline {
  id        String   @id @default(cuid())
  name      String
  isDefault        Boolean  @default(false)
  defaultAssigneeId String?
  defaultAssignee  User?    @relation("defaultPipeline", fields: [defaultAssigneeId], references: [id])
  stages           PipelineStage[]
  deals            Deal[]
  createdAt        DateTime @default(now())
  updatedAt        DateTime @updatedAt
}

model PipelineStage {
  id          String    @id @default(cuid())
  name        String
  position    Int
  color       String
  type        StageType
  probability Int       // 0-100
  slaDays     Int?      // max days before alert
  pipelineId  String
  pipeline    Pipeline  @relation(fields: [pipelineId], references: [id])
  deals       Deal[]
  fromHistory DealStageHistory[] @relation("fromStage")
  toHistory   DealStageHistory[] @relation("toStage")

  @@unique([pipelineId, position])
}

enum StageType { OPEN WON LOST DEFERRED }

model Deal {
  id                  String   @id @default(cuid())
  title               String
  value               Decimal?
  currency            String   @default("PLN")
  stageId             String
  stage               PipelineStage @relation(fields: [stageId], references: [id])
  pipelineId          String
  pipeline            Pipeline @relation(fields: [pipelineId], references: [id])
  companyId           String
  company             Company  @relation(fields: [companyId], references: [id])
  contacts            DealContact[]  // many-to-many with roles
  assignedToId        String
  assignedTo          User     @relation(fields: [assignedToId], references: [id])
  serviceType         ServiceType?
  expectedCloseDate   DateTime?
  lostReasonCategory  LostReasonCategory?
  lostReasonDetails   String?  // optional free text elaboration
  wonDate             DateTime?
  lostDate            DateTime?
  probabilityOverride Int?     // manual override of stage probability
  source              LeadSource?
  activities          Activity[]
  tasks               Task[]
  timeLogs            TimeLog[]
  calendarEvents      CalendarEvent[]
  emailThreads        EmailThread[]
  projects            Project[]
  invoices            Invoice[]
  attachments         Attachment[]
  valueHistory        DealValueHistory[]
  stageHistory        DealStageHistory[]
  tags                TagOnDeal[]
  deletedAt           DateTime?  // soft delete
  stageChangedAt      DateTime @default(now())
  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt

  @@index([stageId])
  @@index([pipelineId])
  @@index([companyId])
  @@index([assignedToId])
}

enum ServiceType {
  DIAGNOSIS
  WORKSHOP
  AUDIT
  TRAINING
  MVP_IMPLEMENTATION
  ENTERPRISE_IMPLEMENTATION
  RETAINER
  COURSE_ONLINE
  OTHER
}

model DealStageHistory {
  id                  String   @id @default(cuid())
  dealId              String
  deal                Deal     @relation(fields: [dealId], references: [id])
  fromStageId         String?
  fromStage           PipelineStage? @relation("fromStage", fields: [fromStageId], references: [id])
  toStageId           String
  toStage             PipelineStage  @relation("toStage", fields: [toStageId], references: [id])
  userId              String
  user                User     @relation(fields: [userId], references: [id])
  durationInStageHours Int?
  changedAt           DateTime @default(now())
}

model DealContact {
  dealId          String
  deal            Deal          @relation(fields: [dealId], references: [id])
  contactPersonId String
  contactPerson   ContactPerson @relation(fields: [contactPersonId], references: [id])
  role            ContactRole   // DECISION_MAKER, CHAMPION, etc.
  isPrimary       Boolean       @default(false)  // main contact for this deal
  @@id([dealId, contactPersonId])
}

enum LostReasonCategory {
  PRICE
  TIMING
  COMPETITOR
  NO_BUDGET
  NO_NEED
  WENT_SILENT
  INTERNAL_CHANGE  // champion left, reorg
  SCOPE_MISMATCH
  OTHER
}

model DealValueHistory {
  id        String   @id @default(cuid())
  dealId    String
  deal      Deal     @relation(fields: [dealId], references: [id])
  oldValue  Decimal?
  newValue  Decimal?
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  reason    String?  // "po negocjacjach zmniejszony zakres"
  changedAt DateTime @default(now())
}
```

### Deal Types & Upsell Tracking

```prisma
enum DealType { NEW_BUSINESS UPSELL RENEWAL CROSS_SELL }

model Deal {
  // ... existing fields ...
  dealType        DealType @default(NEW_BUSINESS)
  parentDealId    String?  // upsell/renewal links back to original deal
  parentDeal      Deal?    @relation("upsell", fields: [parentDealId], references: [id])
  childDeals      Deal[]   @relation("upsell")
  // Recurring (retainer) fields
  isRecurring       Boolean  @default(false)
  recurringValuePln Decimal? // monthly retainer value
  recurringStartDate DateTime?
  recurringEndDate   DateTime? // null = still active
  renewalDate       DateTime? // next renewal check date
}
```

Analytics can now answer: "What % of revenue is new business vs upsell?" and "What is our MRR from retainers?"

### Project Delivery (Post-Sale)

When a Deal reaches "Wygrana", it spawns a Project:

```prisma
model Project {
  id              String        @id @default(cuid())
  name            String        // "Animex — Szkolenie AI Q2"
  dealId          String
  deal            Deal          @relation(fields: [dealId], references: [id])
  companyId       String
  company         Company       @relation(fields: [companyId], references: [id])
  assignedToId    String
  assignedTo      User          @relation(fields: [assignedToId], references: [id])
  status          ProjectStatus @default(ONBOARDING)
  startDate       DateTime?
  targetEndDate   DateTime?
  actualEndDate   DateTime?
  budget          Decimal?      // from deal value
  notes           String?       @db.Text
  milestones      Milestone[]
  activities      Activity[]
  tasks           Task[]
  timeLogs        TimeLog[]
  invoices        Invoice[]
  attachments     Attachment[]
  deletedAt       DateTime?
  createdAt       DateTime      @default(now())
  updatedAt       DateTime      @updatedAt

  @@index([companyId])
  @@index([assignedToId])
  @@index([status])
}

enum ProjectStatus {
  ONBOARDING      // contract signed, kick-off prep
  IN_PROGRESS     // active delivery
  ON_HOLD         // paused (client side or Vesper Rule)
  DELIVERED       // all milestones completed
  IN_RETAINER     // ongoing retainer after delivery
  CANCELLED
}

model Milestone {
  id          String          @id @default(cuid())
  projectId   String
  project     Project         @relation(fields: [projectId], references: [id])
  name        String          // "Audyt procesów", "PoC", "Go-live"
  description String?
  dueDate     DateTime?
  completedAt DateTime?
  status      MilestoneStatus @default(PENDING)
  position    Int             // order within project
  createdAt   DateTime        @default(now())
  updatedAt   DateTime        @updatedAt

  @@unique([projectId, position])
}

enum MilestoneStatus { PENDING IN_PROGRESS COMPLETED SKIPPED }
```

**Default milestones by ServiceType (seeded on project creation):**

| ServiceType | Default Milestones |
|-------------|-------------------|
| TRAINING | Przygotowanie materiałów → Szkolenie dzień 1 → Szkolenie dzień 2 → Ankieta → Raport |
| AUDIT | Kick-off → Zbieranie danych → Analiza → Raport → Prezentacja wyników |
| MVP_IMPLEMENTATION | Kick-off → Audyt procesów → PoC → Implementacja → Testy → Go-live |
| ENTERPRISE_IMPLEMENTATION | Kick-off → Audyt → Architektura → PoC → Faza 1 → Faza 2 → Testy → Go-live → Handover |
| RETAINER | Onboarding → Miesiąc 1 review → Quarterly review (recurring) |

**UI: Project view** (new tab in sidebar after "Czas pracy"):
- List of active projects with status, company, progress bar (completed milestones / total)
- Project detail: milestone timeline (vertical), activity log, tasks, time logged, invoices
- Auto-create project when Deal → Wygrana (with default milestones based on serviceType)

### Invoices & Billing

```prisma
model Invoice {
  id          String        @id @default(cuid())
  dealId      String?
  deal        Deal?         @relation(fields: [dealId], references: [id])
  projectId   String?
  project     Project?      @relation(fields: [projectId], references: [id])
  companyId   String
  company     Company       @relation(fields: [companyId], references: [id])
  number      String?       // iFirma invoice number (e.g. "FV 2026/03/001")
  title       String        // "Szkolenie AI — Animex — Grupa 1"
  amountNet   Decimal
  vatRate     Int           @default(23) // % VAT
  amountGross Decimal?      // computed: net * (1 + vatRate/100)
  currency    String        @default("PLN")
  issuedDate  DateTime?
  dueDate     DateTime?
  paidDate    DateTime?
  status      InvoiceStatus @default(DRAFT)
  externalId  String?       // iFirma ID or Stripe invoice ID
  source      InvoiceSource @default(MANUAL)
  notes       String?
  createdAt   DateTime      @default(now())
  updatedAt   DateTime      @updatedAt

  @@index([companyId])
  @@index([status])
}

enum InvoiceStatus { DRAFT ISSUED SENT PAID OVERDUE CANCELLED }
enum InvoiceSource { MANUAL STRIPE IFIRMA }
```

**Invoice logic:**
- Admin creates invoice in CRM → optionally syncs to iFirma (API) or just stores reference number
- Stripe webhook `invoice.paid` → auto-update CRM Invoice status to PAID
- Deal detail shows: "Wartość: 40 000 PLN | Zafakturowano: 20 000 PLN | Pozostało: 20 000 PLN"
- Project milestones can trigger invoice reminders (e.g. "PoC delivered → invoice 50%")
- Dashboard: outstanding invoices, overdue invoices, revenue collected vs. pipeline

### Client Satisfaction (NPS & Surveys)

```prisma
model Company {
  // ... existing fields ...
  npsScore       Int?       // last NPS score (1-10)
  npsUpdatedAt   DateTime?
  trustLevel     Int?       // 1-5 (from Sales Playbook)
}
```

Add to ActivityType enum:
```prisma
enum ActivityType {
  // ... existing types ...
  SURVEY_RECEIVED   // post-training survey result
  PROJECT_MILESTONE // milestone completed
}
```

**Survey integration:**
- `/survey-sync` skill pushes survey results to CRM via External API
- Creates Activity (type: SURVEY_RECEIVED) on the Company with metadata: `{ nps: 4.8, highlights: [...], quotes: [...] }`
- Auto-updates Company.npsScore
- High NPS (>4) → auto-creates Task "Rozważ upsell / poproś o referencję"
- Visible in Company timeline alongside other activities

### Company Status Flow

```
CONTACT → PROSPECT → LEAD → CLIENT → FORMER_CLIENT
   ↑                                        │
   └────────────────────────────────────────┘ (new deal created)
```

- **CONTACT**: Business card, conference contact, no deal opportunity yet. Just stored in CRM.
- **PROSPECT**: Showing interest or qualified by ICP score, but no active deal.
- **LEAD**: Has at least one active Deal in pipeline. Auto-set when Deal is created.
- **CLIENT**: At least one Deal won. Auto-set when Deal → Wygrana.
- **FORMER_CLIENT**: Was a client, all deals closed, no active engagement.

Status transitions are automatic when deals are created/won/lost, but can be manually overridden.

### Default Pipeline Seed

| Stage | Type | Probability | SLA Days | Color |
|-------|------|:-----------:|:--------:|-------|
| Nowy Lead | OPEN | 5 | 2 | #94a3b8 |
| Kontakt | OPEN | 10 | 3 | #3b82f6 |
| Discovery Call | OPEN | 25 | 5 | #8b5cf6 |
| Propozycja | OPEN | 50 | 5 | #f97316 |
| Negocjacje | OPEN | 75 | 7 | #eab308 |
| Wygrana | WON | 100 | — | #22c55e |
| Przegrana | LOST | 0 | — | #ef4444 |
| Odlozona | DEFERRED | 0 | — | #64748b |

### Activities & Timeline

```prisma
model Activity {
  id              String   @id @default(cuid())
  type            ActivityType
  subject         String
  description     String?  @db.Text
  dealId          String?
  deal            Deal?    @relation(fields: [dealId], references: [id])
  companyId       String?
  company         Company? @relation(fields: [companyId], references: [id])
  contactPersonId String?
  contactPerson   ContactPerson? @relation(fields: [contactPersonId], references: [id])
  userId          String
  user            User     @relation(fields: [userId], references: [id])
  durationMinutes Int?
  happenedAt      DateTime
  projectId       String?
  project         Project? @relation(fields: [projectId], references: [id])
  metadata        Json?    // flexible: gmail thread id, calendar link, etc.
  attachments     Attachment[]
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  @@index([dealId])
  @@index([projectId])
  @@index([companyId])
  @@index([happenedAt])
  @@index([userId])
}

enum ActivityType {
  CALL
  EMAIL_SENT
  EMAIL_RECEIVED
  MEETING
  NOTE
  LINKEDIN_MESSAGE
  SMS
  TASK_COMPLETED
  STAGE_CHANGE
  DEAL_CREATED
  DEAL_WON
  DEAL_LOST
  SURVEY_RECEIVED
  PROJECT_MILESTONE
  INVOICE_ISSUED
  INVOICE_PAID
}
```

### Tasks & Follow-ups

```prisma
model Task {
  id              String     @id @default(cuid())
  title           String
  description     String?
  dueDate         DateTime?
  dueTime         String?    // "14:30" format
  priority        TaskPriority
  status          TaskStatus @default(PENDING)
  type            TaskType
  dealId          String?
  deal            Deal?      @relation(fields: [dealId], references: [id])
  projectId       String?
  project         Project?   @relation(fields: [projectId], references: [id])
  companyId       String?
  company         Company?   @relation(fields: [companyId], references: [id])
  contactPersonId String?
  contactPerson   ContactPerson? @relation(fields: [contactPersonId], references: [id])
  assignedToId    String
  assignedTo      User       @relation("assignedTasks", fields: [assignedToId], references: [id])
  createdById     String
  createdBy       User       @relation("createdTasks", fields: [createdById], references: [id])
  completedAt     DateTime?
  recurrence      Json?      // { type: "weekly", interval: 1 }
  createdAt       DateTime   @default(now())
  updatedAt       DateTime   @updatedAt

  @@index([assignedToId])
  @@index([dueDate])
  @@index([status])
}

enum TaskPriority { LOW MEDIUM HIGH URGENT }
enum TaskStatus { PENDING IN_PROGRESS COMPLETED CANCELLED }
enum TaskType { FOLLOW_UP CALL EMAIL MEETING PROPOSAL REVIEW OTHER }
```

### Auto-generated Tasks (Pipeline Triggers)

When a deal changes stage, the system auto-creates tasks:

| Stage entered | Auto-task | Due |
|---------------|-----------|-----|
| Discovery Call | "Przygotuj się na discovery call" | start_date - 1 day |
| Discovery Call (completed) | "Wyślij podsumowanie discovery" | same day |
| Propozycja | "Wyślij ofertę" | +48h |
| Propozycja (no activity 5 days) | "Follow-up oferta" | +5 days |
| Negocjacje | "Sprawdź status negocjacji" | +3 days |
| Any stage > SLA | "Przeterminowany: [deal title]" | immediately |

### Calendar Events

```prisma
model CalendarEvent {
  id              String   @id @default(cuid())
  title           String
  description     String?
  startAt         DateTime
  endAt           DateTime
  location        String?
  meetingLink     String?
  eventType       CalendarEventType
  dealId          String?
  deal            Deal?    @relation(fields: [dealId], references: [id])
  companyId       String?
  company         Company? @relation(fields: [companyId], references: [id])
  contactPersonId String?
  contactPerson   ContactPerson? @relation(fields: [contactPersonId], references: [id])
  userId          String
  user            User     @relation(fields: [userId], references: [id])
  googleEventId   String?  // sync with GCal
  reminderMinutes Int      @default(15)
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
}

enum CalendarEventType { DISCOVERY_CALL FOLLOW_UP PRESENTATION NEGOTIATION TRAINING INTERNAL OTHER }
```

### Time Tracking

```prisma
model TimeLog {
  id              String   @id @default(cuid())
  userId          String
  user            User     @relation(fields: [userId], references: [id])
  dealId          String?
  deal            Deal?    @relation(fields: [dealId], references: [id])
  projectId       String?
  project         Project? @relation(fields: [projectId], references: [id])
  companyId       String?
  company         Company? @relation(fields: [companyId], references: [id])
  description     String
  startedAt       DateTime
  endedAt         DateTime?
  durationMinutes Int?      // null while timer is running, computed on stop
  billable        Boolean  @default(true)
  ratePln         Decimal?
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
}
```

### Gmail Sync

```prisma
model GmailConnection {
  id            String   @id @default(cuid())
  userId        String   @unique
  user          User     @relation(fields: [userId], references: [id])
  accessToken   String
  refreshToken  String
  tokenExpiry   DateTime
  emailAddress  String
  lastSyncAt    DateTime?
  syncEnabled   Boolean  @default(true)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

model EmailThread {
  id              String   @id @default(cuid())
  gmailThreadId   String   @unique
  subject         String
  lastMessageAt   DateTime
  messageCount    Int
  contactPersonId String?
  contactPerson   ContactPerson? @relation(fields: [contactPersonId], references: [id])
  companyId       String?
  company         Company?       @relation(fields: [companyId], references: [id])
  dealId          String?
  deal            Deal?          @relation(fields: [dealId], references: [id])
  messages        EmailMessage[]
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
}

model EmailMessage {
  id            String   @id @default(cuid())
  gmailMsgId    String   @unique
  threadId      String
  thread        EmailThread @relation(fields: [threadId], references: [id])
  from          String
  to            String[]
  cc            String[]
  subject       String
  bodyPreview   String   @db.Text  // first 500 chars
  bodyHtml      String?  @db.Text
  direction     EmailDirection
  receivedAt    DateTime
  createdAt     DateTime @default(now())
}

enum EmailDirection { INBOUND OUTBOUND }
```

**Gmail sync logic:**
1. User connects Google account via OAuth (consent: read-only email access)
2. Background job runs every 5 minutes per connected user
3. Fetches emails from Gmail API — filtered to addresses matching ContactPerson.email in CRM
4. Matches email → ContactPerson → Company → active Deal
5. Creates EmailMessage records + Activity entries in timeline
6. Stores body preview (500 chars) + optional full HTML
7. Never sends, modifies, or deletes emails in Gmail

### Lead Import

```prisma
model LeadImport {
  id           String       @id @default(cuid())
  filename     String
  source       ImportSource
  totalRows    Int
  importedRows Int          @default(0)
  skippedRows  Int          @default(0)
  status       ImportStatus @default(PENDING)
  errors       Json?
  userId       String
  user         User         @relation(fields: [userId], references: [id])
  createdAt    DateTime     @default(now())
}

enum ImportSource { PRACUJ GENERIC_CSV LINKEDIN_EXPORT BUSINESS_CARDS }
enum ImportStatus { PENDING PROCESSING COMPLETED FAILED }
```

### Webhook Events

```prisma
model WebhookEvent {
  id          String        @id @default(cuid())
  source      WebhookSource
  eventType   String
  externalId  String?       // leadId or Stripe event ID — for idempotency
  payload     Json
  status      WebhookStatus @default(RECEIVED)
  error       String?
  receivedAt  DateTime      @default(now())
  processedAt DateTime?

  @@index([source, externalId])
}

enum WebhookSource { DOKODU_WEBSITE STRIPE N8N }
enum WebhookStatus { RECEIVED PROCESSED FAILED }
```

### Tags

```prisma
model Tag {
  id        String   @id @default(cuid())
  name      String   @unique
  color     String?
  companies TagOnCompany[]
  deals     TagOnDeal[]
}

model TagOnCompany {
  companyId String
  tagId     String
  company   Company @relation(fields: [companyId], references: [id])
  tag       Tag     @relation(fields: [tagId], references: [id])
  @@id([companyId, tagId])
}

model TagOnDeal {
  dealId String
  tagId  String
  deal   Deal   @relation(fields: [dealId], references: [id])
  tag    Tag    @relation(fields: [tagId], references: [id])
  @@id([dealId, tagId])
}
```

### Users & RBAC

```prisma
model User {
  id             String   @id @default(cuid())
  name           String
  email          String   @unique
  passwordHash   String
  avatarUrl      String?
  isActive       Boolean  @default(true)
  lastLoginAt    DateTime?
  failedLoginAttempts Int @default(0)
  lockedUntil    DateTime?
  roles          UserRole[]
  assignedProjects Project[]
  assignedDeals  Deal[]
  assignedTasks  Task[]   @relation("assignedTasks")
  createdTasks   Task[]   @relation("createdTasks")
  activities     Activity[]
  timeLogs       TimeLog[]
  calendarEvents CalendarEvent[]
  gmailConnection GmailConnection?
  stageChanges   DealStageHistory[]
  imports        LeadImport[]
  apiKeys        ApiKey[]
  auditLogs      AuditLog[]
  notifications  Notification[]
  attachments    Attachment[]    @relation("uploadedAttachments")
  dealValueChanges DealValueHistory[]
  defaultPipelines Pipeline[] @relation("defaultPipeline")
  assignedCompanies Company[]
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt
}

model Role {
  id          String   @id @default(cuid())
  name        String   @unique
  description String?
  isSystem    Boolean  @default(false) // system roles can't be deleted
  permissions RolePermission[]
  users       UserRole[]
}

model Permission {
  id          String   @id @default(cuid())
  code        String   @unique  // "deals:create"
  group       String            // "deals"
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
```

### Attachments

```prisma
model Attachment {
  id          String   @id @default(cuid())
  filename    String
  originalName String
  mimeType    String
  sizeBytes   Int
  storagePath String   // relative path in storage (local or R2)
  companyId   String?
  company     Company? @relation(fields: [companyId], references: [id])
  dealId      String?
  deal        Deal?    @relation(fields: [dealId], references: [id])
  activityId  String?
  activity    Activity? @relation(fields: [activityId], references: [id])
  uploadedById String
  uploadedBy  User     @relation(fields: [uploadedById], references: [id])
  createdAt   DateTime @default(now())
}
```

Storage strategy: Local disk in Phase 1 (`/uploads/`), migrate to Cloudflare R2 in Phase 2+ (same infra as dokodu.it). Max file size: 25MB. Allowed types: PDF, DOCX, XLSX, PNG, JPG.

### Audit Log

```prisma
model AuditLog {
  id         String   @id @default(cuid())
  userId     String
  user       User     @relation(fields: [userId], references: [id])
  action     String   // "update", "create", "delete", "export", "login"
  entity     String   // "Deal", "Company", "ContactPerson", etc.
  entityId   String
  changes    Json?    // { field: { old: "50000", new: "35000" } }
  ipAddress  String?
  createdAt  DateTime @default(now())

  @@index([entity, entityId])
  @@index([userId])
  @@index([createdAt])
}
```

Audit log is write-only (no updates, no deletes). Captures: all CRUD operations on core entities, login/logout events, data exports, permission changes. Retention: 2 years.

### Notifications

```prisma
model Notification {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  type        NotificationType
  title       String
  message     String
  dealId      String?
  companyId   String?
  taskId      String?
  isRead      Boolean  @default(false)
  readAt      DateTime?
  createdAt   DateTime @default(now())

  @@index([userId, isRead])
}

enum NotificationType {
  TASK_OVERDUE
  SLA_EXCEEDED
  LEAD_ASSIGNED
  DEAL_WON
  DEAL_LOST
  NEW_LEAD_WEBHOOK
  MENTION
}
```

**Triggers:**
- Task past due date → notify assignee
- Deal on stage > SLA days → notify assignee + admin
- New lead from webhook → notify default assignee
- Deal moved to WON/LOST → notify admin
- Admin assigns lead → notify new assignee

**Delivery:** In-app (bell icon with unread count). Email digest for critical notifications (configurable in user settings).

### RODO / GDPR Compliance

```prisma
enum ConsentType {
  FORM_SUBMISSION    // lead z formularza kontaktowego (explicit consent)
  LEGITIMATE_INTEREST // wizytówka, LinkedIn (Art. 6(1)(f) GDPR)
  CONTRACT           // istniejący klient (Art. 6(1)(b) GDPR)
  MANUAL_CONSENT     // zgoda uzyskana ustnie/mailowo
}
```

**Data subject rights implementation:**
- `GET /api/gdpr/export/:contactId` — exports all data about a person (JSON) — requires `settings:manage` permission
- `POST /api/gdpr/anonymize/:contactId` — replaces PII with "ANONYMIZED", keeps statistical data (deal values, stages) — requires `settings:manage`
- `Company.consentType` + `Company.consentDate` — tracks legal basis for processing

**Retention policy:**
- Deals LOST + no activity for 18 months → auto-flag for review
- Admin decides: anonymize or extend retention with justification
- Anonymization preserves: deal value, stage history, win/loss stats (for analytics)
- Anonymization removes: name, email, phone, NIP, company name

### System Settings & API Keys

```prisma
model SystemSetting {
  id        String   @id @default(cuid())
  key       String   @unique  // e.g. "webhook_secret_dokodu", "stripe_webhook_secret"
  value     String
  encrypted Boolean  @default(false)  // true for secrets, API keys
  updatedAt DateTime @updatedAt
}

model ApiKey {
  id          String   @id @default(cuid())
  name        String               // e.g. "Claude Code", "n8n integration"
  keyHash     String   @unique     // bcrypt hash of the key (plain key shown once on creation)
  keyPrefix   String               // first 8 chars for identification: "dk_live_abc..."
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  permissions String[]             // ["deals:read", "companies:read"] — subset of user's perms
  lastUsedAt  DateTime?
  expiresAt   DateTime?
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
}
```

**SystemSetting** stores: webhook secrets, integration API keys (MailerLite, Stripe), feature flags. Encrypted values are decrypted at read time with app-level key.

**ApiKey** authenticates external API calls (header: `X-API-Key`). On creation, plain key shown once. Stored as bcrypt hash. Permissions are a subset of the creating user's permissions.

### Soft Delete Strategy

Company, ContactPerson, and Deal use soft deletes (`deletedAt` field). All queries filter `WHERE deletedAt IS NULL` by default. Hard deletes are never performed — CRM data is auditable. Prisma middleware applies this filter globally.

### API Conventions

**Pagination:** Offset-based. Query params: `?page=1&pageSize=25`. Response envelope:
```json
{ "data": [...], "meta": { "total": 158, "page": 1, "pageSize": 25, "totalPages": 7 } }
```

**Error format:**
```json
{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }
```
HTTP codes: 400 (validation), 401 (unauthenticated), 403 (forbidden), 404 (not found), 409 (conflict), 500 (server).

**Auth strategy:** NextAuth with JWT sessions (stateless, no DB session lookup per request). Token lifetime: 24h, refresh on activity. External API uses `X-API-Key` header — separate auth path, no session.

---

## 5. UI Modules

### Navigation (Sidebar)

Fixed left sidebar — collapsible to icons on narrow screens.

```
Dashboard
Kontakty → Firmy / Osoby
Pipeline (Kanban)
Deale (lista)
Projekty (realizacja)
Faktury
Kalendarz
Zadania
Czas pracy
Analytics
Import
Ustawienia → Pipeline & Stages / Użytkownicy & Role / Integracje
```

### 5.1 Dashboard

CEO overview — the first thing you see after login.

**KPI Cards (top row):**
- Pipeline value (sum of open deals × probability)
- Deals this month (won / lost / open)
- Conversion rate (won / total closed, trailing 90 days)
- Overdue tasks count
- Upcoming meetings (today + tomorrow)

**Sections:**
- My pipeline — mini kanban, top 5 deals per stage
- Tasks due today — checklist with quick-complete
- Recent activities — timeline (who did what)
- SLA alerts — deals exceeding stage SLA
- Unassigned leads — needs attention

### 5.2 Companies

**List view:** DataTable with columns: name, industry, ICP score (color badge), deal count, total value, assignee, last contact date. Filters: ICP score, industry, source, assignee, tag. Bulk actions: assign, tag, export.

**Detail view:** Single page with editable header (name, NIP, industry, website, LinkedIn). Tabbed content:
- Osoby — ContactPerson list with role badges
- Deale — all deals with this company
- Aktywności — chronological timeline (calls, emails, meetings, notes, stage changes)
- Zadania — open tasks related to this company
- Czas — logged hours
- Emaile — synced Gmail threads (if connected)
- Right sidebar: ICP checklist, tags, source, key dates

### 5.3 Pipeline (Kanban)

Drag-and-drop board (DnD Kit). Columns = PipelineStages.

**Deal card:** Title, company name, contact person, value (PLN), days on stage (red if > SLA), assignee avatar, next task indicator.

**Actions:** Drag between columns (confirm on Won/Lost with reason modal). Click card → Sheet slide-over with deal detail. Quick-add deal per column. Filter by: assignee, service type, value range, source.

**Footer:** Weighted pipeline summary — sum of (value × probability) per stage.

### 5.4 Deal Detail

**Header:** Title, value, stage dropdown, expected close date.

**Two-column layout:**
- Left (wide): Activity timeline with quick action bar (+ Note, + Call, + Email, + Meeting, + Task). Each activity shows: type icon, subject, description, who, when, duration.
- Right (sidebar): Stage progress, company link, contact (phone + email click-to-copy), assignee, service type, source, expected close, won/lost date, tags, value, created date, last activity date.

### 5.5 Calendar

Weekly view (default) + day + month. Color-coded event types: discovery (purple), follow-up (blue), presentation (orange), internal (gray). Click event → deal/contact context. Drag to resize/move. Click empty slot → quick create.

**Google Calendar sync:** Two-way. CRM event creates GCal event (with meet link). GCal events from connected account shown read-only.

### 5.6 Tasks

Grouped list: "Przeterminowane", "Dziś", "Jutro", "Ten tydzień", "Później". Filter by: assignee, priority, deal, company, type. Quick complete checkbox. Each task shows: title, due date, priority badge, linked deal/company.

### 5.7 Time Tracking

Weekly timesheet view (Toggl-style). Start/stop timer or manual entry. Link to deal/company (optional). Billable toggle. Weekly summary: hours per company, per deal. Export to CSV.

### 5.8 Analytics

Chart.js dashboards:
- Pipeline funnel — deals per stage, conversion between stages
- Revenue — won deals per month, trend, YTD total
- Win/Loss — ratio, top loss reasons
- Lead sources — deal count and conversion rate per source
- Sales velocity — avg days per stage, avg deal cycle
- Activity metrics — calls/emails/meetings per user per week
- SLA compliance — % deals within SLA per stage

Global filters: date range, assignee, pipeline, service type.

### 5.9 Import

3-step CSV wizard: Upload + preview → column mapping (company, email, phone, industry, score...) → review + execute (with import log: imported/skipped/errors).

Sources: Pracuj.pl export, LinkedIn export, business cards CSV, generic CSV.

### 5.10 Settings

**Pipeline config:** Drag-and-drop reorder stages, add/edit/delete, set probability/SLA/color. Support for multiple pipelines.

**Users & Roles:** User list with roles. Invite flow (email → link → register). Role management: create custom roles, permission checkbox matrix.

**Integrations:** Webhook URL + secret for dokodu.it. Stripe webhook config. Google Calendar OAuth. Gmail OAuth. MailerLite API key. n8n webhook URLs. API keys for external access (Claude/scripts).

---

## 6. API Design

REST API, all routes prefixed with `/api/`. Every endpoint protected by auth middleware + `requirePermission()`.

### Auth
```
POST   /api/auth/login
POST   /api/auth/invite          (admin only)
POST   /api/auth/register        (with invite token)
GET    /api/auth/me
```

### Companies
```
GET    /api/companies             (list, paginated, filterable)
POST   /api/companies
GET    /api/companies/:id
PATCH  /api/companies/:id
DELETE /api/companies/:id
```

### Contacts
```
GET    /api/contacts
POST   /api/contacts
GET    /api/contacts/:id
PATCH  /api/contacts/:id
DELETE /api/contacts/:id
```

### Deals
```
GET    /api/deals                 (list, paginated, filterable)
POST   /api/deals
GET    /api/deals/:id
PATCH  /api/deals/:id
DELETE /api/deals/:id
PATCH  /api/deals/:id/stage      (stage change + auto DealStageHistory + auto tasks)
GET    /api/deals/pipeline        (kanban view data, grouped by stage)
```

### Activities
```
GET    /api/activities            (filterable by deal, company, contact, user, date)
POST   /api/activities
```

### Tasks
```
GET    /api/tasks                 (filterable, grouped by due date)
POST   /api/tasks
PATCH  /api/tasks/:id
PATCH  /api/tasks/:id/complete
DELETE /api/tasks/:id
```

### Calendar
```
GET    /api/calendar/events       (date range query)
POST   /api/calendar/events
PATCH  /api/calendar/events/:id
DELETE /api/calendar/events/:id
POST   /api/calendar/sync-gcal    (trigger manual sync)
```

### Time Logs
```
GET    /api/timelogs              (date range, user, deal filters)
POST   /api/timelogs
PATCH  /api/timelogs/:id
DELETE /api/timelogs/:id
POST   /api/timelogs/start        (start timer)
PATCH  /api/timelogs/stop         (stop timer)
```

### Analytics
```
GET    /api/analytics/pipeline    (funnel data)
GET    /api/analytics/revenue     (monthly won deals)
GET    /api/analytics/sources     (lead source breakdown)
GET    /api/analytics/velocity    (avg days per stage)
GET    /api/analytics/activities  (activity counts per user)
GET    /api/analytics/sla         (SLA compliance)
GET    /api/analytics/mrr         (monthly recurring revenue, churn)
GET    /api/analytics/projects    (delivery time, milestone completion rates)
GET    /api/analytics/invoices    (outstanding, overdue, revenue collected)
GET    /api/analytics/nps         (client satisfaction trends)
```

### Projects
```
GET    /api/projects              (list, filterable by status, company, assignee)
POST   /api/projects              (usually auto-created from Deal Won)
GET    /api/projects/:id
PATCH  /api/projects/:id
PATCH  /api/projects/:id/milestones  (reorder, update, add milestones)
PATCH  /api/projects/:id/milestones/:mid/complete
```

### Invoices
```
GET    /api/invoices              (list, filterable by status, company, deal, project)
POST   /api/invoices
GET    /api/invoices/:id
PATCH  /api/invoices/:id
DELETE /api/invoices/:id
GET    /api/invoices/summary      (outstanding, overdue, collected totals)
```

### Tags
```
GET    /api/tags
POST   /api/tags
PATCH  /api/tags/:id
DELETE /api/tags/:id
POST   /api/companies/:id/tags    (assign tag)
DELETE /api/companies/:id/tags/:tagId
POST   /api/deals/:id/tags
DELETE /api/deals/:id/tags/:tagId
```

### Notifications
```
GET    /api/notifications         (current user, with ?unread=true filter)
PATCH  /api/notifications/:id/read
POST   /api/notifications/read-all
```

### Attachments
```
POST   /api/attachments           (multipart upload, linked to company/deal/project/activity)
GET    /api/attachments/:id       (download)
DELETE /api/attachments/:id
```

### Audit Log
```
GET    /api/audit-log             (admin only, filterable by entity, user, date range)
```

### GDPR
```
GET    /api/gdpr/export/:contactId   (export all PII as JSON)
POST   /api/gdpr/anonymize/:contactId (replace PII, keep stats)
```

### Import
```
POST   /api/import/upload         (CSV upload + preview)
POST   /api/import/execute        (run mapped import)
GET    /api/import/history        (past imports)
```

### Webhooks (incoming)
```
POST   /api/webhooks/dokodu       (lead from website form, verified by secret)
POST   /api/webhooks/stripe       (payment events)
```

### Gmail Sync
```
POST   /api/gmail/connect         (initiate OAuth flow)
GET    /api/gmail/callback        (OAuth callback)
POST   /api/gmail/disconnect
GET    /api/gmail/threads         (synced threads for a contact/company)
POST   /api/gmail/sync            (trigger manual sync)
```

### Settings
```
GET    /api/pipelines
POST   /api/pipelines
PATCH  /api/pipelines/:id
PATCH  /api/pipelines/:id/stages  (reorder, add, edit stages)

GET    /api/roles
POST   /api/roles
PATCH  /api/roles/:id
PATCH  /api/roles/:id/permissions

GET    /api/users
PATCH  /api/users/:id
DELETE /api/users/:id             (deactivate)
```

### External API (for Claude Code / scripts)
```
GET    /api/external/deals        (API key auth via header)
GET    /api/external/companies
GET    /api/external/contacts
GET    /api/external/analytics
POST   /api/external/leads        (push lead programmatically)
```

---

## 7. Integrations

### 7.1 dokodu.it Webhook

dokodu.it sends POST to `/api/webhooks/dokodu` on lead capture.

**Payload:**
```json
{
  "secret": "shared_webhook_secret",
  "leadId": "clx...",
  "name": "Jan Kowalski",
  "email": "jan@firma.pl",
  "phone": "+48...",
  "company": "Firma Sp. z o.o.",
  "website": "https://firma.pl",
  "context": "Szukamy automatyzacji procesów HR...",
  "source": "contact_form",
  "utmSource": "linkedin",
  "utmMedium": "post",
  "createdAt": "2026-03-29T10:00:00Z"
}
```

**CRM processing:** Verify secret → upsert Company (by name/NIP) → upsert ContactPerson (by email) → create Deal (stage: "Nowy Lead") → create Activity (type: DEAL_CREATED) → auto-assign to default user (or round-robin if configured).

### 7.2 Stripe Webhook

Stripe sends payment events to `/api/webhooks/stripe`.

**Events handled:**
- `checkout.session.completed` → find Deal by customer email → update metadata
- `invoice.paid` → log as Activity on matching Deal

### 7.3 Gmail API (read-only sync)

- OAuth 2.0 with Google Workspace
- Scopes: `gmail.readonly`
- Background job: every 5 minutes per connected user
- Filters: only fetches threads involving email addresses present in ContactPerson table
- Stores: subject, from, to, cc, preview (500 chars), full HTML (optional), timestamps
- Creates Activity entries (EMAIL_SENT / EMAIL_RECEIVED) in timeline
- Never sends, modifies, or deletes emails

### 7.4 Google Calendar (two-way sync)

- OAuth 2.0 with Google Calendar API
- Scopes: `calendar.events`
- CRM → GCal: creating CalendarEvent in CRM pushes to Google Calendar
- GCal → CRM: sync back changes (time, cancellation)
- Meeting links auto-generated (Google Meet)

### 7.5 MailerLite

- On deal stage change to WON → add contact to "Klienci" group
- On deal LOST → add to "Nurturing" group
- API key configured in settings

### 7.6 n8n Webhooks

- Configurable outgoing webhooks on events: deal_created, deal_stage_changed, deal_won, deal_lost, task_overdue
- Enables custom automation flows in n8n

### 7.7 External API (Claude Code / Scripts)

- API key authentication (header: `X-API-Key`)
- Read endpoints for deals, companies, contacts, analytics
- Write endpoint for pushing leads programmatically
- Used by Claude Code skills (brain-status, brain-add-lead, outreach) to read/write CRM data

---

## 8. UI Design Guidelines

**Theme:** White, light, modern — in the style of dokodu.it but optimized for dashboard use.

- **Background:** White (#ffffff) with light gray (#f8fafc) for cards and sidebar
- **Primary accent:** Dokodu navy/dark blue with blue accent highlights
- **Typography:** Inter (or system font stack) — clean, readable at small sizes
- **Spacing:** Generous whitespace, consistent 4px grid
- **Corners:** Rounded (8px cards, 6px buttons, 4px inputs)
- **Shadows:** Subtle (shadow-sm on cards, shadow-md on modals)
- **Icons:** Lucide React (consistent with dokodu.it)
- **Responsive:** Desktop-first (internal tool), but usable on tablet
- **Components:** shadcn/ui — DataTable, Command (Cmd+K), Sheet, Dialog, Select, Tabs, Badge, Calendar

---

## 9. Implementation Phases

### Phase 1: Foundation (MVP)
- Project setup (Next.js, Prisma, PostgreSQL, NextAuth, shadcn/ui)
- RBAC system (roles, permissions, scope-based data isolation, middleware)
- User management + invite flow
- Company CRUD with status flow (CONTACT → PROSPECT → LEAD → CLIENT)
- ContactPerson CRUD (many-to-many with deals via DealContact)
- Pipeline configuration (stages, SLA, colors)
- Deal CRUD + Kanban board + DealValueHistory
- LostReason categorization (enum + optional details)
- Activity timeline (manual: notes, calls, meetings)
- Attachment upload (local storage, linked to company/deal)
- Audit log (all CRUD operations)
- RODO: consent tracking on Company, anonymization endpoint
- Global search (Cmd+K — companies, contacts, deals, full-text PostgreSQL)
- Basic dashboard (KPI cards + task list)
- Data migration script (existing BRAIN data + dokodu.it leads)

### Phase 2: Productivity & Post-Sale
- Task system (CRUD + auto-generation on stage change)
- Project delivery module (Project + Milestones, auto-create on Deal Won)
- Invoice tracking (CRUD, link to Deal/Project, status tracking)
- Calendar module (weekly/day/month views)
- Google Calendar two-way sync
- Time tracking module (linked to projects and deals)
- CSV import wizard (Pracuj, LinkedIn, generic) + duplicate detection
- Webhook receiver (dokodu.it → auto-create deals) with idempotency key
- Notifications system (in-app + email digest for critical)
- Duplicate detection + merge flow (match by NIP, email, company name)
- External API (for Claude Code skills — brain-status, brain-add-lead, outreach)

### Phase 3: Intelligence
- Gmail API read-only sync
- Email threads in timeline
- Analytics dashboards (pipeline funnel, revenue, MRR, sources, velocity, SLA, project delivery)
- Survey integration (NPS → Company, auto-upsell tasks)
- Retainer management dashboard (MRR, renewal dates, churn)
- Stripe webhook integration
- MailerLite integration (segment on stage change)
- iFirma sync (invoice numbers, payment status)
- RODO: retention policy auto-flagging (18 months inactive)

### Phase 4: Automation & Scale
- n8n outgoing webhooks
- Auto-task rules (configurable triggers)
- Advanced filters + saved views
- Bulk actions (assign, tag, stage change)
- Export (CSV, PDF reports) — Admin only
- Attachment storage migration to Cloudflare R2
- Custom fields (JSON schema per entity type — Company, Deal, Project)

---

## 10. Key Design Decisions

1. **Separate project** — CRM has different users, different lifecycle, different deployment cadence than dokodu.it
2. **Webhook integration** — dokodu.it pushes leads to CRM via webhook. CRM is single source of truth for sales data.
3. **Gmail read-only** — no sending from CRM. Professional email stays in Gmail. CRM only displays history.
4. **Configurable pipeline** — stages, probabilities, SLA are admin-configurable, not hardcoded
5. **RBAC with strict data isolation** — Sales sees ONLY own assigned records (companies, contacts, deals, values). Cannot see other salespeople's pipeline or deal values. Cannot export data. Admin sees all. Search results are scope-filtered.
6. **API-first** — every feature has REST API. Enables Claude Code integration and future mobile app.
7. **Activity-centric** — everything that happens is an Activity. Timeline is the core UX pattern.
8. **Contact ≠ Lead** — Company starts as CONTACT (business card, no opportunity). Becomes LEAD only when a Deal is created. This prevents polluting the pipeline with unqualified contacts while keeping them accessible in the CRM.
9. **Many-to-many deals↔contacts** — B2B deals involve multiple stakeholders (decision maker, champion, blocker). DealContact pivot tracks who plays what role in each deal.
10. **Full audit trail** — Every data change is logged (AuditLog). Deal value changes have dedicated history (DealValueHistory). Stage changes have DealStageHistory. Nothing is lost.
11. **RODO by design** — Consent type tracked per company. Anonymization endpoint preserves analytics while removing PII. Retention auto-flagging after 18 months of inactivity.

---

## 11. Data Security Model

### Scope Isolation (Critical)

The Sales role is **sandboxed**. Every database query for a Sales user automatically applies:

```
WHERE assignedToId = :currentUserId
```

**What Sales CAN see:**
- Companies assigned to them
- Contacts within those companies
- Deals assigned to them (and their values)
- Activities they created or on their deals/companies
- Tasks assigned to them
- Time logs they created

**What Sales CANNOT see:**
- Other salespeople's companies, contacts, or deals
- Pipeline total value (only their own weighted pipeline)
- Other users' activities or tasks
- Analytics beyond their own performance
- Export/CSV features

**What Sales CANNOT do:**
- Export any data (no CSV, no PDF reports)
- Bulk actions on non-assigned records
- Access RBAC settings, pipeline configuration, or user management
- Change their own role or permissions

**Implementation:** Prisma middleware applies scope filter on every query. API endpoints validate scope. UI components hide elements based on permissions. Global search returns only records within user's scope.

### Data Loss Prevention

- No bulk data export for non-Admin roles
- API key permissions are a subset of the creating user's permissions (Admin creates key with limited scope)
- Session timeout: 8 hours inactivity → auto-logout
- Failed login attempts: lock after 5 failures for 15 minutes
- AuditLog tracks all data exports with IP address

---

## 12. Data Migration Plan (Phase 1)

### Sources to migrate:

1. **BRAIN CRM data** (`DOKODU_BRAIN/20_AREAS/AREA_Customers/`)
   - 3 customer profiles (Animex, Corleonis, Korollo) → Company + ContactPerson + Deal records
   - Status: CLIENT (Animex, Corleonis), PROSPECT (Korollo)

2. **BRAIN Lead Qualification** (`Lead_Qualification_Full_2026-03-29.md`)
   - 158 scored companies → Company records with ICP score (A/B/C/X)
   - Status: CONTACT (no active deal yet)

3. **dokodu.it Lead table** (PostgreSQL)
   - Existing leads from website forms → Company + ContactPerson + Deal (stage: based on current status)
   - One-time migration, then webhook takes over

4. **Outreach Tracker** (if populated by then)
   - LinkedIn contacts → ContactPerson records

### Migration script:
- Python or TypeScript script, runs once
- Deduplicates by email/NIP/company name
- Maps existing statuses to new pipeline stages
- Creates initial Activity records ("Imported from [source]")
- Dry-run mode first, then execute with admin approval

---

## 13. Global Search (Cmd+K)

PostgreSQL full-text search with `tsvector` columns on:
- `Company.name`, `Company.nip`, `Company.city`
- `ContactPerson.firstName`, `ContactPerson.lastName`, `ContactPerson.email`
- `Deal.title`
- `Activity.subject`, `Activity.description`

**Search behavior:**
- Debounce: 300ms
- Results grouped by type: Companies, Contacts, Deals
- Each result shows: name, type badge, status/stage, assignee
- Click → navigate to detail page
- **Scope-filtered**: Sales users only see results from their assigned records
- Max 5 results per type, "See all" link for full search page

---

## 14. Webhook Idempotency

dokodu.it webhook payload includes `leadId` (unique identifier from source system).

**Deduplication logic:**
```
1. Receive webhook → check WebhookEvent table for same source + leadId
2. If exists and status = PROCESSED → return 200 OK, skip processing
3. If not exists → create WebhookEvent, process, mark PROCESSED
```

This prevents duplicate deals when dokodu.it retries on timeout.
