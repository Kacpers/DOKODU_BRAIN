# Plan 6: Bulletproof PII Inventory (Codegen + CI Gate + Runtime View)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development.

**Goal:** Build automated GDPR data-map system from spec section "Bulletproof Personal Data Inventory". Source of truth = Prisma schema annotations. Drift = blocked by CI.

**Why:** RODO compliance. Each new field that holds personal data must be classified (basic/sensitive/special-category) with retention + lawful basis. Currently this is tribal knowledge — engineer can add a field without RODO consideration.

---

## Files

### Created
- `scripts/gen-data-map.ts` — codegen: parse `schema.prisma` → write `docs/data-map.md`
- `scripts/verify-pii-annotations.ts` — CI gate: error if any field lacks `@pii` or `@no-pii`
- `src/app/api/gdpr/data-map/route.ts` — runtime endpoint serving the map as JSON
- `src/app/(app)/settings/data-inventory/page.tsx` — UI rendering the map
- `.github/workflows/pii-check.yml` (or `.husky/pre-commit`) — enforce gate
- `docs/data-map.md` — first generated output (then auto-updated)

### Modified
- `prisma/schema.prisma` — add `///` annotations to every field (~70 fields)
- `package.json` — `gen:data-map` + `verify:pii-annotations` scripts
- `prisma/seed.ts` (no change — but `User` model gets `@pii basic` etc.)

---

## Annotation syntax

Prisma supports triple-slash `///` doc comments. We use these for metadata:

```prisma
model ContactPerson {
  /// @pii basic
  /// @retention 7y after deletion
  /// @lawful-basis contract
  /// @export-as identifier
  /// @anonymize hash
  firstName String

  /// @no-pii
  isPrimary Boolean @default(false)
}
```

Categories:
- `@pii basic` — name, email, phone (most common)
- `@pii sensitive` — special category (health, ethnicity, religion, etc.)
- `@pii internal` — internal data referencing PII (audit logs, change history)
- `@no-pii` — explicitly non-PII (technical fields, IDs, booleans)

Required fields when `@pii` is set:
- `@retention` — how long retained (e.g., `7y after deletion`, `30d post consent withdraw`)
- `@lawful-basis` — `contract`, `legitimate-interest`, `consent`, `legal-obligation`
- `@export-as` — `identifier` (verbatim) or `hash` (hashed for export) or `redact`
- `@anonymize` — `nullify`, `hash`, `randomize`, `keep-aggregated`

---

## Tasks (high-level)

1. Schema parser — read schema.prisma, extract field metadata + annotations
2. `gen-data-map.ts` — produce `docs/data-map.md` (markdown table per model + computed properties: total field count, PII count by category)
3. `verify-pii-annotations.ts` — fail if any field missing required annotations
4. Annotate ALL existing fields (Companies, Contacts, Deals, Activities, Tasks, etc. — ~70 fields total)
5. CI workflow / pre-commit hook
6. Runtime API endpoint
7. UI page in settings
8. DPA template referencing live `/settings/data-inventory` URL

---

## Out of scope

- Automatic GDPR deletion request handling (manual via Prisma Studio for now)
- Multi-language data map (PL only)
- PII discovery in JSON Json fields (e.g., `Company.icpFitReasons: Json`) — manual annotation if known to contain PII
- Encryption-at-rest for sensitive fields (separate Plan 7 task)

---

## Open questions

- Annotation enforcement strictness: hard-fail CI or soft-warn? Recommend hard-fail to drive culture.
- For Json fields with PII inside (e.g., notes that may contain personal info): require explicit `@pii basic` even if JSON shape varies?
- DPA reference URL — should it be public (anyone can view) or auth'd (only this client's admin)?
