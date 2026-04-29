# Plan 4: Cmd+K AI Parser + AI Widgets

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Implement the WOW-factor demo feature — Cmd+K input where user types natural language ("Klient ABC chce szkolenie z Gemini w Q2, przypomnij tydzień przed") and AI parses → preview cards → confirm → creates entities in transaction.

**Architecture:**
- Frontend: `<CmdKModal>` component with input + preview cards. Triggered by `⌘K` shortcut OR top-bar button. Wraps existing `cmdk` library (`cmdk@^1.1.1` already in deps).
- API: `POST /api/ai/parse-intent` (Anthropic Claude Sonnet 4.6 + function calling) → returns array of tool calls. `POST /api/ai/execute-intent` runs them in Prisma transaction.
- Tool definitions: `src/lib/ai/tools.ts` — Zod schemas for `createDeal`, `createTask`, `createReminder`, `createMeeting`, `addNote`, `createCompany`, `createContact`, `linkToEntity`.
- AI widgets in cards: 3 actions per entity card (`Streszcz`, `Napisz follow-up`, `Co dalej?`) — separate routes.
- BYOK: Anthropic API key from `SystemSetting` (encrypted) or `ANTHROPIC_API_KEY` env. Default: server's key.

**Tech:** `@anthropic-ai/sdk@^0.91.1` (already added). React 19 + Next.js 16 App Router.

---

## Files

### Created
- `src/lib/ai/anthropic-client.ts` — singleton client with BYOK support
- `src/lib/ai/tools.ts` — Zod tool schemas + Anthropic tool definitions
- `src/lib/ai/parse-intent.ts` — main parsing logic (extracted from route for testability)
- `src/lib/ai/execute-intent.ts` — execution logic (Prisma transactions)
- `src/lib/ai/__tests__/tools.test.ts`
- `src/lib/ai/__tests__/parse-intent.test.ts` (mocked Anthropic)
- `src/app/api/ai/parse-intent/route.ts` — POST handler
- `src/app/api/ai/execute-intent/route.ts` — POST handler
- `src/app/api/ai/summarize-deal/route.ts` — AI widget endpoint
- `src/app/api/ai/draft-followup/route.ts` — AI widget endpoint
- `src/app/api/ai/next-steps/route.ts` — AI widget endpoint
- `src/components/cmdk/cmdk-modal.tsx` — main modal component
- `src/components/cmdk/cmdk-trigger.tsx` — top-bar button + ⌘K hotkey
- `src/components/cmdk/preview-card.tsx` — single action preview
- `src/components/ai-widgets/ai-widget-buttons.tsx` — 3-button widget for entity cards

### Modified
- `src/components/layout/app-shell.tsx` — wrap with `<CmdKProvider>` + add trigger button
- `src/components/layout/topbar.tsx` — add Cmd+K button (or new file if not exists)

---

## Task 1: Tool schemas (Zod + Anthropic format)

**Files:** `src/lib/ai/tools.ts`, `src/lib/ai/__tests__/tools.test.ts`

- [ ] **Step 1: TDD — write failing test**

```typescript
// src/lib/ai/__tests__/tools.test.ts
import { describe, it, expect } from 'vitest';
import { TOOLS, parseToolCall } from '../tools';

describe('TOOLS', () => {
  it('exports all 8 tools', () => {
    const names = TOOLS.map((t) => t.name);
    expect(names).toContain('createDeal');
    expect(names).toContain('createTask');
    expect(names).toContain('createReminder');
    expect(names).toContain('createMeeting');
    expect(names).toContain('addNote');
    expect(names).toContain('createCompany');
    expect(names).toContain('createContact');
    expect(names).toContain('linkToEntity');
    expect(names).toHaveLength(8);
  });

  it('every tool has Anthropic-compatible schema', () => {
    for (const tool of TOOLS) {
      expect(tool.name).toMatch(/^[a-zA-Z]+$/);
      expect(tool.description).toBeTruthy();
      expect(tool.input_schema.type).toBe('object');
      expect(tool.input_schema.properties).toBeDefined();
    }
  });
});

describe('parseToolCall', () => {
  it('validates createDeal args', () => {
    const result = parseToolCall('createDeal', {
      title: 'Test',
      companyName: 'Acme',
      value: 50000,
    });
    expect(result.success).toBe(true);
  });

  it('rejects createDeal without title', () => {
    const result = parseToolCall('createDeal', { companyName: 'Acme' });
    expect(result.success).toBe(false);
  });

  it('rejects unknown tool name', () => {
    const result = parseToolCall('unknownTool', {});
    expect(result.success).toBe(false);
  });
});
```

- [ ] **Step 2: Implement `src/lib/ai/tools.ts`**

```typescript
import { z } from 'zod';

const dealSchema = z.object({
  title: z.string().min(1),
  companyName: z.string().min(1).optional(),
  companyId: z.string().optional(),
  value: z.number().optional(),
  expectedCloseDate: z.string().optional(),
  stage: z.string().optional(),
});

const taskSchema = z.object({
  title: z.string().min(1),
  dueDate: z.string().optional(),
  assigneeId: z.string().optional(),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH', 'URGENT']).optional(),
  relatedToType: z.enum(['Company', 'Deal', 'ContactPerson']).optional(),
  relatedToId: z.string().optional(),
});

const reminderSchema = z.object({
  title: z.string().min(1),
  datetime: z.string(),
  channel: z.enum(['email', 'push']).default('push'),
});

const meetingSchema = z.object({
  title: z.string().min(1),
  datetime: z.string(),
  attendees: z.array(z.string()).optional(),
  location: z.string().optional(),
});

const noteSchema = z.object({
  text: z.string().min(1),
  relatedToType: z.enum(['Company', 'Deal', 'ContactPerson']),
  relatedToId: z.string().min(1),
});

const companySchema = z.object({
  name: z.string().min(1),
  industry: z.string().optional(),
  source: z.enum(['MANUAL', 'WEBSITE_FORM', 'LINKEDIN', 'REFERRAL', 'COLD_CALL', 'CONFERENCE']).default('MANUAL'),
});

const contactSchema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  email: z.string().email().optional(),
  phone: z.string().optional(),
  companyId: z.string().optional(),
  companyName: z.string().optional(),
});

const linkSchema = z.object({
  fromType: z.enum(['Company', 'Deal', 'ContactPerson']),
  fromId: z.string(),
  toType: z.enum(['Company', 'Deal', 'ContactPerson']),
  toId: z.string(),
});

const TOOL_SCHEMAS = {
  createDeal: dealSchema,
  createTask: taskSchema,
  createReminder: reminderSchema,
  createMeeting: meetingSchema,
  addNote: noteSchema,
  createCompany: companySchema,
  createContact: contactSchema,
  linkToEntity: linkSchema,
} as const;

export type ToolName = keyof typeof TOOL_SCHEMAS;

// Anthropic tool definitions (input_schema is JSON Schema)
export const TOOLS = [
  {
    name: 'createDeal',
    description: 'Create a new sales deal/opportunity in the pipeline',
    input_schema: {
      type: 'object',
      properties: {
        title: { type: 'string', description: 'Deal title' },
        companyName: { type: 'string', description: 'Company name (will be looked up or created)' },
        companyId: { type: 'string', description: 'Company ID if known' },
        value: { type: 'number', description: 'Estimated value in PLN' },
        expectedCloseDate: { type: 'string', description: 'ISO date string (YYYY-MM-DD)' },
        stage: { type: 'string', description: 'Pipeline stage name' },
      },
      required: ['title'],
    },
  },
  // ... other tools follow same pattern (truncated — full spec in actual implementation)
] as const;

export interface ToolCallResult<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
}

export function parseToolCall(name: string, args: unknown): ToolCallResult {
  if (!(name in TOOL_SCHEMAS)) {
    return { success: false, error: `Unknown tool: ${name}` };
  }
  const schema = TOOL_SCHEMAS[name as ToolName];
  const result = schema.safeParse(args);
  if (!result.success) {
    return { success: false, error: result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ') };
  }
  return { success: true, data: result.data };
}
```

- [ ] **Step 3: Run tests**

```bash
pnpm test src/lib/ai/__tests__/tools.test.ts
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add src/lib/ai/
git commit -m "feat(crm): AI tool definitions for Cmd+K parser"
```

---

## Task 2: Parse intent (Anthropic call + dispatch)

**Files:** `src/lib/ai/parse-intent.ts`, `src/lib/ai/__tests__/parse-intent.test.ts`

- [ ] **Step 1: Implement `src/lib/ai/parse-intent.ts`**

```typescript
import Anthropic from '@anthropic-ai/sdk';
import { TOOLS, parseToolCall, type ToolName } from './tools';

export interface ParseIntentInput {
  userText: string;
  context: {
    currentDate: string;
    userId: string;
    currentEntity?: { type: string; id: string };
  };
}

export interface ToolCall {
  name: ToolName;
  args: Record<string, unknown>;
  reasoning?: string;
}

export interface ParseIntentResult {
  toolCalls: ToolCall[];
  rawResponse: string;
}

const SYSTEM_PROMPT = `You are an assistant that translates natural language CRM commands into structured tool calls. The user types in Polish; respond by calling the appropriate tools. Always include a brief reasoning. Never create entities without explicit user request — if intent is unclear, return zero tool calls and explain in reasoning.`;

export async function parseIntent(opts: ParseIntentInput, apiKey: string): Promise<ParseIntentResult> {
  const client = new Anthropic({ apiKey });

  const message = await client.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 2048,
    system: SYSTEM_PROMPT,
    tools: [...TOOLS],
    messages: [
      {
        role: 'user',
        content: `Context:
- Current date: ${opts.context.currentDate}
- User ID: ${opts.context.userId}
${opts.context.currentEntity ? `- Currently viewing: ${opts.context.currentEntity.type}/${opts.context.currentEntity.id}` : ''}

Command: ${opts.userText}`,
      },
    ],
  });

  const toolCalls: ToolCall[] = [];
  let reasoning = '';

  for (const block of message.content) {
    if (block.type === 'text') {
      reasoning += block.text;
    } else if (block.type === 'tool_use') {
      const validation = parseToolCall(block.name, block.input);
      if (validation.success) {
        toolCalls.push({
          name: block.name as ToolName,
          args: validation.data as Record<string, unknown>,
          reasoning: reasoning.trim() || undefined,
        });
        reasoning = '';
      }
    }
  }

  return {
    toolCalls,
    rawResponse: message.content.map((b) => (b.type === 'text' ? b.text : '')).join(''),
  };
}
```

- [ ] **Step 2: Test (mocked Anthropic)**

```typescript
import { describe, it, expect, vi } from 'vitest';
import { parseIntent } from '../parse-intent';

vi.mock('@anthropic-ai/sdk', () => ({
  default: vi.fn().mockImplementation(() => ({
    messages: {
      create: vi.fn().mockResolvedValue({
        content: [
          { type: 'text', text: 'User wants to create a deal for ABC.' },
          {
            type: 'tool_use',
            name: 'createDeal',
            input: { title: 'Test Deal', companyName: 'ABC', value: 50000 },
          },
        ],
      }),
    },
  })),
}));

describe('parseIntent', () => {
  it('parses tool call from Anthropic response', async () => {
    const result = await parseIntent(
      {
        userText: 'Klient ABC chce zlecenie 50k',
        context: { currentDate: '2026-04-29', userId: 'user1' },
      },
      'fake-key'
    );

    expect(result.toolCalls).toHaveLength(1);
    expect(result.toolCalls[0].name).toBe('createDeal');
    expect(result.toolCalls[0].args.title).toBe('Test Deal');
  });
});
```

- [ ] **Step 3: Run tests + commit**

```bash
pnpm test src/lib/ai/__tests__/parse-intent.test.ts
git add src/lib/ai/
git commit -m "feat(crm): parseIntent with Anthropic + tool calling"
```

---

## Task 3: Execute intent (Prisma transaction)

**Files:** `src/lib/ai/execute-intent.ts`, `src/lib/ai/__tests__/execute-intent.test.ts`

[Truncated for brevity — implementation iterates over tool calls and creates entities in `prisma.$transaction`. Each tool has its own creator function (e.g. `createDealHandler`, `createTaskHandler`). Companies are looked up by `companyName` and created if not found. Returns array of created entity IDs.]

---

## Task 4: API routes

**Files:** `src/app/api/ai/parse-intent/route.ts`, `src/app/api/ai/execute-intent/route.ts`

[Each route:
- POST handler
- requirePermission check
- Read API key from SystemSetting or env
- Call parseIntent / executeIntent
- Return JSON response]

---

## Task 5: AI widgets routes

**Files:** `src/app/api/ai/summarize-deal/route.ts`, `draft-followup/route.ts`, `next-steps/route.ts`

[Each route:
- Takes entity ID
- Reads activities/deals from DB
- Calls Anthropic for summary/email/next-steps
- Caches result for 1h in `SystemSetting` or in-memory]

---

## Task 6: Cmd+K modal component

**Files:** `src/components/cmdk/cmdk-modal.tsx`, `src/components/cmdk/preview-card.tsx`

[CmdK library wraps `cmdk@^1.1.1`:
- Modal with input
- On submit → POST /api/ai/parse-intent
- Display preview cards (one per tool call)
- Each card: title, args (editable inline), accept/reject toggle
- Footer: "Anuluj" / "Utwórz wszystkie"
- On confirm → POST /api/ai/execute-intent
- Show success toast + close]

---

## Task 7: Cmd+K trigger + integration

**Files:** `src/components/cmdk/cmdk-trigger.tsx`, modifications to app-shell

[Top-bar button + ⌘K shortcut. Renders modal via CmdKProvider context.]

---

## Task 8: AI widget buttons in entity cards

**Files:** `src/components/ai-widgets/ai-widget-buttons.tsx`

[3 buttons: Streszcz / Napisz follow-up / Co dalej?
On click → relevant API route → display result in dialog or inline.]

---

## Final verification

- [ ] `pnpm test` — all AI tests pass
- [ ] `pnpm build` — no errors
- [ ] Manual smoke test on master demo (after Plan 2 stabilizes login):
  - Open ⌘K
  - Type: "Klient ABC chce szkolenie w Q2, przypomnij tydzień przed"
  - See preview with createDeal + createTask + createReminder
  - Click "Utwórz wszystkie"
  - Verify entities exist in Prisma Studio

## Out of scope

- Streaming responses (return all at once for now)
- Tool call retries on validation failure
- Per-user AI usage tracking (Plan 7 reliability)
- Semantic search via pgvector (Plan 4.5 — separate task)
- BYOK config UI (Plan 5)

## Open questions

- AI provider toggle (Anthropic vs OpenAI vs Voyage) — start with Anthropic, plug-in others later
- Default for demo instances — use Dokodu's API key (rate-limited per instance) vs require user's
- Streaming — improves perceived latency but complicates state mgmt
