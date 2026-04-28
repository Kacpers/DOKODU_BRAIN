# Theme-from-URL + First Demo Deploy (Plan 2/7)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable `/crm-new-demo {url}` BRAIN command to produce a working themed demo at `dev.dokodu.it/crm-{slug}` within ~5 minutes — including reverse-nginx routing, industry-appropriate seed data, and tweak-preview UI for last-mile color adjustment. After Plan 2, Kacper can run `/crm-new-demo pedrollo.pl` and have a live, brand-matched, data-populated CRM ready for sales presentation.

**Architecture:** Multi-step pipeline orchestrated by a BRAIN skill:

1. **Theme-from-URL** — Playwright fetches the prospect's website, extracts logo / colors / fonts; Claude Haiku polishes the palette; output lands in `themes/{slug}/`.
2. **Tweak preview** — local browser-based UI shows a sample dashboard in the new theme with inline color pickers; Kacper accepts or adjusts.
3. **Deploy** — generates `docker-compose.{slug}.yml` from the template (Plan 1), builds image with `BUILD_BASE_PATH=/crm-{slug}`, brings up containers, runs migrations + seed.
4. **Reverse-nginx** — adds path-based route `dev.dokodu.it/crm-{slug}/` → `crm-{slug}:3001` on the Dokodu serwer; reloads nginx.
5. **Seed bundles** — industry-appropriate sample data (Pedrollo = `distribution-b2b` bundle in this plan; HABA / `water-treatment` deferred).
6. **BRAIN skille** — `/crm-new-demo` end-to-end orchestrator + `/crm-status` instance dashboard.

**Tech Stack:** Adds Playwright (~250 MB browsers — installed once on dev machine, NOT in production image), Sharp (image processing), `@anthropic-ai/sdk` (AI polish via Claude Haiku), envsubst (already on Linux). Server-side: existing reverse-nginx in `/srv/reverse-proxy/conf.d/`, `web` Docker network, wildcard cert `*.dokodu.it`.

**Working directories:**
- Local: `/Users/ksieradzinski/Projects/dokodu/crm-new` (CRM repo, where most code goes)
- BRAIN skille: `/Users/ksieradzinski/Projects/dokodu/brain-public/.claude/skills/`
- Server: `deploy@57.128.219.9:/srv/reverse-proxy/` (nginx) + `~deploy/crm-instances/` (compose files + themes)

**Estimated effort:** 2-3 dni roboty, 15 atomic tasks. TDD na warstwie ekstrakcji (kolory, logo, font); smoke testy end-to-end na deploy.

**Pre-merge dependency:** Plan 1 PR #1 zmergowany do `main` w crm-new (commit `7503226`). Plan 2 buduje na fundamencie multi-instance.

---

## File Structure

### Created — local (crm-new repo)
- `scripts/theme-from-url.ts` — main CLI entry (orchestration)
- `scripts/theme-from-url/fetch-brand.ts` — Playwright fetcher
- `scripts/theme-from-url/extract-colors.ts` — k-means pixel extraction
- `scripts/theme-from-url/extract-logo.ts` — logo finder + downloader (Sharp)
- `scripts/theme-from-url/extract-fonts.ts` — font detection from computed styles
- `scripts/theme-from-url/ai-polish.ts` — Claude Haiku integration
- `scripts/theme-from-url/__tests__/extract-colors.test.ts`
- `scripts/theme-from-url/__tests__/extract-fonts.test.ts`
- `scripts/theme-tweak.ts` — preview server (Express + simple HTML, port 3099)
- `scripts/deploy-instance.sh` — orchestrate compose generation + build + up + migrate + seed
- `scripts/destroy-instance.sh` — cleanup (containers, volumes, theme dir)
- `scripts/list-instances.sh` — JSON output for `/crm-status`
- `scripts/lib/slug-from-url.ts` — URL → slug mapping (used by theme + deploy)
- `seed-bundles/_lib/factories.ts` — typed factory functions (createCompany, createDeal, ...)
- `seed-bundles/_lib/load-bundle.ts` — bundle dispatcher
- `seed-bundles/distribution-b2b/seed.ts` — Pedrollo-shaped data
- `seed-bundles/distribution-b2b/README.md` — what's in this bundle and when to use

### Created — BRAIN repo (brain-public)
- `.claude/skills/crm-new-demo/SKILL.md` — orchestrator
- `.claude/skills/crm-status/SKILL.md` — instance dashboard

### Created — server (Dokodu serwer)
- `/srv/reverse-proxy/conf.d/crm-instances.conf` — path-based routing (deployed by `deploy-instance.sh` first time, idempotent)

### Modified
- `package.json` — add Playwright, Sharp, @anthropic-ai/sdk, express, ws (preview server)
- `prisma/seed.ts` — dispatch to bundle from env `SEED_BUNDLE`
- `src/middleware.ts` — fix `new URL("/login", origin)` to respect basePath (Plan 2 prereq from review)
- `src/app/api/health/route.ts` — use `db` import (CLAUDE.md convention; Plan 1 minor follow-up)
- `src/lib/modules.ts` — drop misleading `sorted` local var
- `src/lib/theme.ts` — add TODO comments for unused fields (typography wiring deferred to Plan 5)
- `.dockerignore` — exclude `__tests__/`, `vitest.config.ts`, `vitest.setup.ts`, `docs/`, `seed-bundles/_lib/`
- `CLAUDE.md` (crm-new) — add scripts/ section

---

## Task 1: Plan 1 follow-ups polish

**Why:** Bundle the small follow-ups from Plan 1's final review into one focused commit so they don't get lost. Clean foundation for the rest of Plan 2.

**Files:**
- Modify: `src/middleware.ts` — fix `new URL("/login", origin)` to use basePath
- Modify: `src/app/api/health/route.ts` — `import { db as prisma }` per convention
- Modify: `src/lib/modules.ts` — drop `sorted` rename, just `[...enabled]` inline
- Modify: `src/lib/theme.ts` — add `// TODO(plan-5): wire typography to layout font loader` and `// TODO(plan-5): handle logoDarkUrl when darkMode is on`
- Modify: `.dockerignore` — add exclusions

- [ ] **Step 1: Read middleware.ts to find the basePath issue**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
grep -n 'new URL\|nextUrl\|redirect' src/middleware.ts
```

Expected: at least one `new URL("/login", origin)` or `nextUrl.pathname` check that doesn't account for basePath. Note exact line numbers.

- [ ] **Step 2: Fix middleware basePath handling**

For each `new URL("/login", origin)` (or similar literal redirect path), prepend `process.env.BASE_PATH ?? ''`:

```typescript
// Before
return NextResponse.redirect(new URL("/login", origin));

// After
const basePath = process.env.BASE_PATH ?? '';
return NextResponse.redirect(new URL(`${basePath}/login`, origin));
```

For `nextUrl.pathname` checks (e.g. `if (pathname === '/login')`), strip the basePath prefix first or compare against full path. Approach: at top of middleware, normalize:

```typescript
const basePath = process.env.BASE_PATH ?? '';
const pathname = req.nextUrl.pathname.startsWith(basePath)
  ? req.nextUrl.pathname.slice(basePath.length) || '/'
  : req.nextUrl.pathname;
```

Then use `pathname` for routing decisions; build redirect URLs with `basePath` prepended.

- [ ] **Step 3: Build with BASE_PATH set, smoke test middleware**

```bash
DATABASE_URL=postgresql://test/test BASE_PATH=/crm-test pnpm build 2>&1 | tail -5
```

Expected: build success.

- [ ] **Step 4: Update /api/health to use `db` import**

Edit `src/app/api/health/route.ts`:

```typescript
// Before
import { prisma } from '@/lib/prisma';
// After
import { db as prisma } from '@/lib/prisma';
```

(Alias to `prisma` keeps the rest of the route + tests unchanged.)

- [ ] **Step 5: Verify health route tests still pass**

```bash
pnpm test src/app/api/health/__tests__/route.test.ts
```

Expected: 2 tests pass. (The mock targets `@/lib/prisma`'s `prisma` export — but `db` is also exported from there. Verify the test uses the right name.)

If the mock breaks — adjust mock to export both `prisma` and `db` aliases:

```typescript
vi.mock('@/lib/prisma', () => ({
  prisma: { $queryRaw: mockQueryRaw },
  db: { $queryRaw: mockQueryRaw },
}));
```

- [ ] **Step 6: Drop misleading `sorted` local var in modules.ts**

Edit `src/lib/modules.ts` `createModuleRegistry`:

```typescript
// Before
export function createModuleRegistry(enabled: string[]): ModuleRegistry {
  const set = new Set(enabled);
  const sorted = [...enabled];
  return {
    isEnabled(name: string): boolean { return set.has(name); },
    list(): readonly string[] { return sorted; },
  };
}

// After
export function createModuleRegistry(enabled: string[]): ModuleRegistry {
  const set = new Set(enabled);
  const ordered = Object.freeze([...enabled]);
  return {
    isEnabled(name: string): boolean { return set.has(name); },
    list(): readonly string[] { return ordered; },
  };
}
```

Run modules tests:

```bash
pnpm test src/lib/__tests__/modules.test.ts
```

Expected: 6 tests pass.

- [ ] **Step 7: Add TODO comments to theme.ts**

In `src/lib/theme.ts`, find `typography` and `logoDarkUrl` fields in the schema and add inline comments:

```typescript
brand: z.object({
  name: z.string().min(1, 'brand.name required'),
  logoUrl: z.string().min(1),
  // TODO(plan-5): wire logoDarkUrl when darkMode is enabled in UI
  logoDarkUrl: z.string().optional(),
  favicon: z.string().min(1),
}),
// ...
// TODO(plan-5): wire to layout's next/font/google loader (currently hardcoded Plus_Jakarta_Sans)
typography: z
  .object({
    heading: z.string(),
    body: z.string(),
  })
  .optional(),
```

- [ ] **Step 8: Update .dockerignore**

```
node_modules
.next
.env.local
.git
**/__tests__
**/*.test.ts
vitest.config.ts
vitest.setup.ts
docs
.env.example
seed-bundles/_lib/__tests__
```

(Don't exclude `themes/` or `seed-bundles/{bundle}/seed.ts` — those need to ship in the image.)

- [ ] **Step 9: Run full test suite + build**

```bash
pnpm test && \
DATABASE_URL=postgresql://test/test pnpm build 2>&1 | tail -3
```

Expected: 29 tests pass; build success.

- [ ] **Step 10: Commit**

```bash
git add src/middleware.ts src/app/api/health/route.ts src/app/api/health/__tests__/route.test.ts src/lib/modules.ts src/lib/theme.ts .dockerignore
git commit -m "fix(crm): Plan 1 follow-ups — middleware basePath, db import, .dockerignore, TODOs"
```

---

## Task 2: Theme-from-URL CLI scaffold + slug-from-url helper

**Why:** Establish the CLI entry point and the URL → slug mapping. The slug is used everywhere (theme dir, container name, BASE_PATH, nginx route), so it MUST be deterministic and validated against the same regex as `BASE_PATH_REGEX` from Plan 1.

**Files:**
- Create: `scripts/theme-from-url.ts` (main entry, orchestrates fetch → extract → polish → write)
- Create: `scripts/lib/slug-from-url.ts` (pure function with tests)
- Create: `scripts/lib/__tests__/slug-from-url.test.ts`
- Modify: `package.json` — add Playwright + Sharp + @anthropic-ai/sdk + commander deps + `theme:from-url` script

- [ ] **Step 1: Install dependencies**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm add playwright sharp @anthropic-ai/sdk commander
pnpm add -D @types/sharp
pnpm exec playwright install chromium
```

Expected: packages installed, Chromium downloaded (~150 MB cache in `~/Library/Caches/ms-playwright/`).

- [ ] **Step 2: Write the failing test for slug-from-url**

Create `scripts/lib/__tests__/slug-from-url.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { slugFromUrl } from '../slug-from-url';

describe('slugFromUrl', () => {
  it('extracts slug from simple URL', () => {
    expect(slugFromUrl('https://pedrollo.pl')).toBe('pedrollo');
  });

  it('strips www. prefix', () => {
    expect(slugFromUrl('https://www.pedrollo.pl')).toBe('pedrollo');
  });

  it('strips http and https consistently', () => {
    expect(slugFromUrl('http://pedrollo.pl')).toBe('pedrollo');
    expect(slugFromUrl('https://pedrollo.pl')).toBe('pedrollo');
  });

  it('uses second-level domain only', () => {
    expect(slugFromUrl('https://pedrollo.pl/about')).toBe('pedrollo');
    expect(slugFromUrl('https://shop.pedrollo.pl')).toBe('pedrollo');
  });

  it('handles multi-word brands with hyphens', () => {
    expect(slugFromUrl('https://baselinker.com')).toBe('baselinker');
    expect(slugFromUrl('https://my-company.pl')).toBe('my-company');
  });

  it('lowercases', () => {
    expect(slugFromUrl('https://Pedrollo.PL')).toBe('pedrollo');
  });

  it('rejects URLs that produce invalid slugs', () => {
    expect(() => slugFromUrl('https://invalid_slug.pl')).toThrow(/slug/);
    expect(() => slugFromUrl('not-a-url')).toThrow();
  });

  it('result matches BASE_PATH_REGEX (single segment, lowercase, no underscores)', () => {
    const slug = slugFromUrl('https://pedrollo.pl');
    expect(`/crm-${slug}`).toMatch(/^\/[a-z0-9-]+$/);
  });
});
```

Run tests, confirm fail:

```bash
pnpm test scripts/lib/__tests__/slug-from-url.test.ts
```

Expected: FAIL — module not found.

- [ ] **Step 3: Implement slug-from-url.ts**

Create `scripts/lib/slug-from-url.ts`:

```typescript
import { BASE_PATH_REGEX } from '@/lib/base-path';

/**
 * Convert a website URL to a deterministic slug used as instance identifier.
 *
 * Examples:
 *   pedrollo.pl       → "pedrollo"
 *   www.pedrollo.pl   → "pedrollo"
 *   shop.pedrollo.pl  → "pedrollo"  (second-level domain only)
 *   baselinker.com    → "baselinker"
 *   my-company.pl     → "my-company"
 *
 * The slug must be valid for use in `/crm-{slug}` URLs, so it's validated
 * against BASE_PATH_REGEX. Underscores, uppercase, dots, etc. are rejected.
 */
export function slugFromUrl(input: string): string {
  let url: URL;
  try {
    // Ensure URL has a protocol for the parser
    const withProto = input.startsWith('http') ? input : `https://${input}`;
    url = new URL(withProto);
  } catch {
    throw new Error(`Invalid URL: "${input}"`);
  }

  // Strip www. and take second-level domain
  let host = url.hostname.toLowerCase().replace(/^www\./, '');
  // hostname like "shop.pedrollo.pl" → take "pedrollo" (second-from-last)
  const parts = host.split('.');
  const slug = parts.length >= 2 ? parts[parts.length - 2] : parts[0];

  // Validate the produced slug works as a BASE_PATH segment
  const candidate = `/${slug}`;
  if (!BASE_PATH_REGEX.test(candidate)) {
    throw new Error(
      `URL "${input}" produces invalid slug "${slug}" — must be lowercase letters/digits/hyphens only`
    );
  }

  return slug;
}
```

- [ ] **Step 4: Run tests, verify pass**

```bash
pnpm test scripts/lib/__tests__/slug-from-url.test.ts
```

Expected: 8 tests pass.

- [ ] **Step 5: Create CLI scaffold (orchestrator only — Tasks 3-7 fill in stages)**

Create `scripts/theme-from-url.ts`:

```typescript
#!/usr/bin/env tsx
import { Command } from 'commander';
import { slugFromUrl } from './lib/slug-from-url';
import { resolve } from 'path';
import { mkdirSync, existsSync } from 'fs';

interface BuildThemeOptions {
  url: string;
  outDir: string;
  skipAi: boolean;
  verbose: boolean;
}

async function buildTheme(opts: BuildThemeOptions): Promise<void> {
  const slug = slugFromUrl(opts.url);
  const outPath = resolve(opts.outDir, slug);

  if (!existsSync(outPath)) mkdirSync(outPath, { recursive: true });

  console.log(`[theme-from-url] slug: ${slug}`);
  console.log(`[theme-from-url] output: ${outPath}`);

  // Stages added in Tasks 3-7:
  // 1. const brand = await fetchBrand(opts.url, { verbose: opts.verbose });   // Task 3
  // 2. const colors = extractColors(brand.screenshot);                        // Task 4
  // 3. const logoFile = await extractLogo(brand, outPath);                    // Task 5
  // 4. const fonts = extractFonts(brand.computedStyles);                      // Task 6
  // 5. const polished = opts.skipAi ? colors : await aiPolish({ ... });       // Task 7
  // 6. writeThemeJson(outPath, { brand: { name, logoFile, ... }, polished, fonts, ... });

  throw new Error('Not yet implemented — see Tasks 3-7');
}

const program = new Command();
program
  .name('theme-from-url')
  .description('Generate a Dokodu CRM theme from a website URL')
  .argument('<url>', 'website URL, e.g. https://pedrollo.pl')
  .option('-o, --out-dir <dir>', 'output directory', './themes')
  .option('--skip-ai', 'skip Claude Haiku polish step (use raw extraction)', false)
  .option('-v, --verbose', 'verbose logging', false)
  .action(async (url, options) => {
    try {
      await buildTheme({ url, ...options });
    } catch (err) {
      console.error(`[theme-from-url] FAILED: ${err instanceof Error ? err.message : err}`);
      process.exit(1);
    }
  });

program.parseAsync();
```

- [ ] **Step 6: Add npm script**

In `package.json` `scripts`:

```json
"theme:from-url": "tsx scripts/theme-from-url.ts"
```

Verify CLI runs:

```bash
pnpm theme:from-url --help
```

Expected: shows usage. Do NOT actually try to build a theme yet — Tasks 3-7 fill in.

- [ ] **Step 7: Commit**

```bash
git add scripts/theme-from-url.ts scripts/lib/slug-from-url.ts scripts/lib/__tests__/slug-from-url.test.ts package.json pnpm-lock.yaml
git commit -m "feat(crm): theme-from-url CLI scaffold + slugFromUrl with shared regex"
```

---

## Task 3: Brand fetcher (Playwright)

**Why:** First real stage of theme-from-URL — fetch the prospect's homepage with a real browser, capture screenshot for color extraction, and dump computed styles for font detection.

**Files:**
- Create: `scripts/theme-from-url/fetch-brand.ts`
- Create: `scripts/theme-from-url/__tests__/fetch-brand.test.ts` (smoke test only — full Playwright tests are slow)

- [ ] **Step 1: Define the FetchBrandResult type and interface**

Create `scripts/theme-from-url/fetch-brand.ts`:

```typescript
import { chromium, Browser, Page } from 'playwright';

export interface FetchBrandResult {
  /** Final URL after redirects */
  url: string;
  /** PNG screenshot of viewport (1440x900) — Buffer */
  homepageScreenshot: Buffer;
  /** Logo candidates discovered in DOM, in priority order */
  logoCandidates: string[];
  /** Favicon URL */
  favicon: string | null;
  /** Computed styles for typography detection */
  computedStyles: {
    heading: { fontFamily: string; fontWeight: string };
    body: { fontFamily: string; fontWeight: string };
  };
  /** All hex/rgb colors found in CSS variables (best-effort) */
  cssVariableColors: string[];
}

interface FetchOpts {
  verbose: boolean;
  timeout?: number;
}

export async function fetchBrand(url: string, opts: FetchOpts): Promise<FetchBrandResult> {
  const log = (msg: string) => opts.verbose && console.log(`[fetch-brand] ${msg}`);
  const browser: Browser = await chromium.launch({ headless: true });
  try {
    const ctx = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      userAgent:
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
        '(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    });
    const page = await ctx.newPage();

    log(`navigating to ${url}`);
    const response = await page.goto(url, {
      waitUntil: 'networkidle',
      timeout: opts.timeout ?? 30_000,
    });
    if (!response || !response.ok()) {
      throw new Error(`fetch failed: ${response?.status() ?? 'no response'}`);
    }
    const finalUrl = page.url();

    // Wait a beat for any deferred CSS/JS
    await page.waitForTimeout(1500);

    log('screenshot');
    const homepageScreenshot = await page.screenshot({ fullPage: false });

    log('extracting logo candidates');
    const logoCandidates = await page.evaluate(() => {
      const candidates: string[] = [];
      // Priority 1: <link rel="icon"> with reasonable size
      const linkIcons = Array.from(
        document.querySelectorAll('link[rel*="icon"]')
      ) as HTMLLinkElement[];
      candidates.push(...linkIcons.map((l) => l.href).filter(Boolean));
      // Priority 2: og:image
      const og = document.querySelector('meta[property="og:image"]');
      if (og) candidates.push((og as HTMLMetaElement).content);
      // Priority 3: <header> img / nav img
      const headerImgs = Array.from(
        document.querySelectorAll('header img, nav img')
      ) as HTMLImageElement[];
      candidates.push(...headerImgs.map((i) => i.src).filter(Boolean));
      return candidates;
    });

    log('extracting favicon');
    const favicon = await page.evaluate(() => {
      const link = document.querySelector(
        'link[rel="icon"], link[rel="shortcut icon"]'
      ) as HTMLLinkElement | null;
      return link?.href ?? null;
    });

    log('extracting computed styles');
    const computedStyles = await page.evaluate(() => {
      const heading = document.querySelector('h1, h2');
      const body = document.body;
      const get = (el: Element | null) => {
        if (!el) return { fontFamily: 'sans-serif', fontWeight: '400' };
        const cs = getComputedStyle(el);
        return { fontFamily: cs.fontFamily, fontWeight: cs.fontWeight };
      };
      return { heading: get(heading), body: get(body) };
    });

    log('extracting CSS variable colors');
    const cssVariableColors = await page.evaluate(() => {
      const root = document.documentElement;
      const styles = getComputedStyle(root);
      const colors: string[] = [];
      for (let i = 0; i < styles.length; i++) {
        const prop = styles[i];
        if (prop.startsWith('--')) {
          const value = styles.getPropertyValue(prop).trim();
          if (/^#[0-9a-fA-F]{3,8}$|^rgb/.test(value)) colors.push(value);
        }
      }
      return Array.from(new Set(colors));
    });

    return {
      url: finalUrl,
      homepageScreenshot,
      logoCandidates: Array.from(new Set(logoCandidates)),
      favicon,
      computedStyles,
      cssVariableColors,
    };
  } finally {
    await browser.close();
  }
}
```

- [ ] **Step 2: Write smoke test (live network — gated behind env var)**

Create `scripts/theme-from-url/__tests__/fetch-brand.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { fetchBrand } from '../fetch-brand';

const ONLINE = process.env.ONLINE_TESTS === '1';

describe.skipIf(!ONLINE)('fetchBrand (live network — set ONLINE_TESTS=1)', () => {
  it('fetches example.com brand info', async () => {
    const result = await fetchBrand('https://example.com', { verbose: false });
    expect(result.url).toContain('example.com');
    expect(result.homepageScreenshot.length).toBeGreaterThan(1000);
    expect(result.computedStyles.body.fontFamily).toBeTruthy();
  }, 60_000);
});

describe('fetchBrand (offline)', () => {
  it('throws on invalid URL', async () => {
    await expect(fetchBrand('not-a-url', { verbose: false })).rejects.toThrow();
  });
});
```

- [ ] **Step 3: Run tests (default skips ONLINE)**

```bash
pnpm test scripts/theme-from-url/__tests__/fetch-brand.test.ts
```

Expected: 1 test passes (offline), 1 skipped.

- [ ] **Step 4: Manual smoke test (run once locally)**

```bash
ONLINE_TESTS=1 pnpm test scripts/theme-from-url/__tests__/fetch-brand.test.ts
```

Expected: 2 tests pass, including live fetch from example.com (~5 sec).

- [ ] **Step 5: Wire fetchBrand into theme-from-url.ts orchestrator**

In `scripts/theme-from-url.ts`, replace the `throw new Error('Not yet implemented')` line with:

```typescript
const brand = await import('./theme-from-url/fetch-brand').then((m) =>
  m.fetchBrand(opts.url, { verbose: opts.verbose })
);

console.log(`[theme-from-url] fetched: ${brand.url}`);
console.log(`[theme-from-url] logo candidates: ${brand.logoCandidates.length}`);
console.log(`[theme-from-url] CSS var colors: ${brand.cssVariableColors.length}`);

// Tasks 4-7 will use `brand` for color/logo/font/AI stages
throw new Error('Stages 2-5 not yet implemented — see Tasks 4-7');
```

Smoke test:

```bash
pnpm theme:from-url https://example.com 2>&1 | head -10
```

Expected: prints fetched URL, candidate counts; then exits with the "Stages 2-5 not yet implemented" error.

- [ ] **Step 6: Commit**

```bash
git add scripts/theme-from-url/fetch-brand.ts scripts/theme-from-url/__tests__/fetch-brand.test.ts scripts/theme-from-url.ts
git commit -m "feat(crm): Playwright-based brand fetcher for theme-from-url"
```

---

## Task 4: Color extraction (k-means)

**Why:** Pull dominant brand colors from the homepage screenshot. Filter out neutrals (white, near-white, near-black) so what's returned is actually brand-distinctive.

**Files:**
- Create: `scripts/theme-from-url/extract-colors.ts`
- Create: `scripts/theme-from-url/__tests__/extract-colors.test.ts`

- [ ] **Step 1: Write the failing tests**

Create `scripts/theme-from-url/__tests__/extract-colors.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { extractColors, isNearNeutral, hexFromRgb } from '../extract-colors';

describe('hexFromRgb', () => {
  it('formats 0,0,0 as #000000', () => {
    expect(hexFromRgb([0, 0, 0])).toBe('#000000');
  });
  it('formats 255,255,255 as #ffffff', () => {
    expect(hexFromRgb([255, 255, 255])).toBe('#ffffff');
  });
  it('pads single-digit hex', () => {
    expect(hexFromRgb([1, 2, 3])).toBe('#010203');
  });
});

describe('isNearNeutral', () => {
  it('detects near-white as neutral', () => {
    expect(isNearNeutral([250, 250, 252])).toBe(true);
  });
  it('detects near-black as neutral', () => {
    expect(isNearNeutral([5, 5, 5])).toBe(true);
  });
  it('detects gray as neutral', () => {
    expect(isNearNeutral([128, 128, 128])).toBe(true);
  });
  it('detects pure red as NOT neutral', () => {
    expect(isNearNeutral([230, 57, 70])).toBe(false);
  });
  it('detects strong blue as NOT neutral', () => {
    expect(isNearNeutral([15, 33, 55])).toBe(false);
  });
});

describe('extractColors', () => {
  it('returns at most maxColors brand colors', async () => {
    // Create a tiny test image: 2x2 pixel buffer with 4 distinct colors
    // This is a minimal PNG of 2x2 pixels: red, blue, white, black
    // Use Sharp to generate it programmatically.
    const sharp = (await import('sharp')).default;
    const img = await sharp({
      create: {
        width: 4, height: 1,
        channels: 3, background: { r: 0, g: 0, b: 0 },
      },
    })
      .raw()
      .toBuffer();
    // Manually paint pixels: [red][blue][white][black]
    img[0] = 255; img[1] = 0; img[2] = 0;
    img[3] = 0; img[4] = 0; img[5] = 255;
    img[6] = 255; img[7] = 255; img[8] = 255;
    img[9] = 0; img[10] = 0; img[11] = 0;
    const png = await sharp(img, { raw: { width: 4, height: 1, channels: 3 } })
      .png()
      .toBuffer();

    const colors = await extractColors(png, { maxColors: 3 });
    expect(colors.length).toBeLessThanOrEqual(3);
    // White and black should be filtered as neutral; red and blue remain
    const hexValues = colors.map((c) => c.hex);
    expect(hexValues).toContain('#ff0000');
    expect(hexValues).toContain('#0000ff');
  });

  it('returns empty array for all-neutral image', async () => {
    const sharp = (await import('sharp')).default;
    const png = await sharp({
      create: {
        width: 100, height: 100, channels: 3,
        background: { r: 250, g: 250, b: 252 },
      },
    }).png().toBuffer();
    const colors = await extractColors(png, { maxColors: 5 });
    expect(colors).toEqual([]);
  });
});
```

- [ ] **Step 2: Run, verify fail**

```bash
pnpm test scripts/theme-from-url/__tests__/extract-colors.test.ts
```

Expected: FAIL — module missing.

- [ ] **Step 3: Implement extract-colors.ts**

Create `scripts/theme-from-url/extract-colors.ts`:

```typescript
import sharp from 'sharp';

export type Rgb = [number, number, number];

export interface ColorWithCount {
  hex: string;
  rgb: Rgb;
  count: number;
}

export interface ExtractOpts {
  /** Max distinct colors to return after filtering */
  maxColors: number;
  /** Down-sample image to N pixels max (for speed). Default: 16384 (= 128x128) */
  sampleSize?: number;
  /** Lightness threshold for neutral detection (default 0.92 = >92% means near-white). */
  neutralLightThreshold?: number;
  /** Lightness threshold for darkness (default 0.08 = <8% means near-black). */
  neutralDarkThreshold?: number;
  /** Saturation threshold for grayness (default 0.08 = <8% means desaturated). */
  neutralSatThreshold?: number;
}

/**
 * Convert RGB triplet to lower-cased hex string `#rrggbb`.
 */
export function hexFromRgb([r, g, b]: Rgb): string {
  const h = (n: number) => n.toString(16).padStart(2, '0');
  return `#${h(r)}${h(g)}${h(b)}`;
}

/**
 * True if the color is too close to white/black/gray to count as a brand color.
 * Uses HSL: a color is "neutral" if lightness is extreme OR saturation is too low.
 */
export function isNearNeutral(
  rgb: Rgb,
  opts: { lightThreshold?: number; darkThreshold?: number; satThreshold?: number } = {}
): boolean {
  const { lightThreshold = 0.92, darkThreshold = 0.08, satThreshold = 0.08 } = opts;
  const [r, g, b] = rgb.map((c) => c / 255);
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const lightness = (max + min) / 2;
  if (lightness >= lightThreshold || lightness <= darkThreshold) return true;
  if (max === min) return true; // pure gray
  const d = max - min;
  const sat = lightness > 0.5 ? d / (2 - max - min) : d / (max + min);
  return sat < satThreshold;
}

/**
 * Quantize each RGB channel to multiples of 8 (256 / 8 = 32 buckets per channel,
 * total 32^3 ≈ 32k buckets). Reduces near-duplicate colors before counting.
 */
function quantize([r, g, b]: Rgb): Rgb {
  return [r & 0b11111000, g & 0b11111000, b & 0b11111000];
}

/**
 * Extract dominant non-neutral colors from an image buffer.
 * Algorithm: down-sample → quantize → count → filter neutrals → sort by frequency.
 */
export async function extractColors(
  pngBuffer: Buffer,
  opts: ExtractOpts
): Promise<ColorWithCount[]> {
  const targetSize = Math.sqrt(opts.sampleSize ?? 16384);
  const { data, info } = await sharp(pngBuffer)
    .resize(Math.round(targetSize), Math.round(targetSize), { fit: 'inside' })
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const counts = new Map<string, ColorWithCount>();
  for (let i = 0; i < data.length; i += info.channels) {
    const rgb: Rgb = [data[i], data[i + 1], data[i + 2]];
    const q = quantize(rgb);
    if (
      isNearNeutral(q, {
        lightThreshold: opts.neutralLightThreshold,
        darkThreshold: opts.neutralDarkThreshold,
        satThreshold: opts.neutralSatThreshold,
      })
    ) {
      continue;
    }
    const hex = hexFromRgb(q);
    const existing = counts.get(hex);
    if (existing) {
      existing.count++;
    } else {
      counts.set(hex, { hex, rgb: q, count: 1 });
    }
  }

  return Array.from(counts.values())
    .sort((a, b) => b.count - a.count)
    .slice(0, opts.maxColors);
}
```

- [ ] **Step 4: Run tests, verify pass**

```bash
pnpm test scripts/theme-from-url/__tests__/extract-colors.test.ts
```

Expected: 11 tests pass (3 hexFromRgb + 5 isNearNeutral + 2 extractColors + 1 sentinel may vary).

- [ ] **Step 5: Wire into theme-from-url.ts**

In `scripts/theme-from-url.ts` orchestrator, replace the placeholder error with:

```typescript
const colors = await import('./theme-from-url/extract-colors').then((m) =>
  m.extractColors(brand.homepageScreenshot, { maxColors: 6 })
);
console.log(`[theme-from-url] extracted ${colors.length} brand colors:`);
colors.forEach((c) => console.log(`   ${c.hex} (count=${c.count})`));

// Tasks 5-7 will use `colors`, `brand.logoCandidates`, `brand.computedStyles`
throw new Error('Stages 3-5 not yet implemented — see Tasks 5-7');
```

Smoke test:

```bash
pnpm theme:from-url https://pedrollo.pl 2>&1 | head -15
```

Expected: prints 1-6 brand color hexes from Pedrollo's homepage. Pedrollo's brand red `#e30613` (or close) should be among them.

- [ ] **Step 6: Commit**

```bash
git add scripts/theme-from-url/extract-colors.ts scripts/theme-from-url/__tests__/extract-colors.test.ts scripts/theme-from-url.ts
git commit -m "feat(crm): k-means color extraction with neutral filtering"
```

---

## Task 5: Logo extraction + download (Sharp)

**Why:** Each instance needs its prospect's logo as `themes/{slug}/logo.{ext}`. We pick the best candidate from `brand.logoCandidates`, download it, and save to disk.

**Files:**
- Create: `scripts/theme-from-url/extract-logo.ts`
- Create: `scripts/theme-from-url/__tests__/extract-logo.test.ts`

- [ ] **Step 1: Write the failing tests (focus on URL ranking, not actual downloads)**

Create `scripts/theme-from-url/__tests__/extract-logo.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { rankLogoCandidates, inferExtension } from '../extract-logo';

describe('rankLogoCandidates', () => {
  it('prefers SVG over PNG over JPG', () => {
    const ranked = rankLogoCandidates([
      'https://example.com/logo.jpg',
      'https://example.com/logo.svg',
      'https://example.com/logo.png',
    ]);
    expect(ranked[0]).toContain('.svg');
    expect(ranked[1]).toContain('.png');
    expect(ranked[2]).toContain('.jpg');
  });

  it('prefers same-host candidates over CDN', () => {
    const ranked = rankLogoCandidates(
      [
        'https://cdn.thirdparty.com/logo.png',
        'https://example.com/static/logo.png',
      ],
      'https://example.com'
    );
    expect(ranked[0]).toContain('example.com');
  });

  it('deduplicates', () => {
    const ranked = rankLogoCandidates([
      'https://example.com/logo.png',
      'https://example.com/logo.png',
    ]);
    expect(ranked).toHaveLength(1);
  });

  it('filters non-HTTP URLs (data:, blob:)', () => {
    const ranked = rankLogoCandidates([
      'data:image/png;base64,iVBOR...',
      'https://example.com/logo.png',
      'blob:https://example.com/abc',
    ]);
    expect(ranked).toEqual(['https://example.com/logo.png']);
  });
});

describe('inferExtension', () => {
  it('returns svg for .svg URL', () => {
    expect(inferExtension('https://example.com/logo.svg')).toBe('svg');
  });
  it('returns png for .png URL', () => {
    expect(inferExtension('https://example.com/logo.png?v=2')).toBe('png');
  });
  it('returns webp for .webp URL', () => {
    expect(inferExtension('https://example.com/logo.webp')).toBe('webp');
  });
  it('falls back to png for unknown extension', () => {
    expect(inferExtension('https://example.com/logo')).toBe('png');
  });
});
```

- [ ] **Step 2: Run, verify fail**

```bash
pnpm test scripts/theme-from-url/__tests__/extract-logo.test.ts
```

Expected: FAIL — module missing.

- [ ] **Step 3: Implement extract-logo.ts**

Create `scripts/theme-from-url/extract-logo.ts`:

```typescript
import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

export interface ExtractLogoResult {
  /** Filename written under outDir (e.g. "logo.svg" or "logo.png") */
  filename: string;
  /** Full path on disk */
  fullPath: string;
  /** Whether we downsized/converted (vs. saving raw) */
  processed: boolean;
}

const EXT_PRIORITY: Record<string, number> = {
  svg: 100,
  png: 50,
  webp: 30,
  jpg: 10,
  jpeg: 10,
  gif: 5,
  ico: 1,
};

export function inferExtension(url: string): string {
  const m = url.match(/\.([a-z]{3,4})(?:\?|#|$)/i);
  if (!m) return 'png';
  const ext = m[1].toLowerCase();
  return ext in EXT_PRIORITY ? ext : 'png';
}

/**
 * Rank logo candidates by quality:
 *   1. Filter out non-HTTP URLs (data:, blob:, javascript:)
 *   2. Deduplicate
 *   3. Sort by extension preference (SVG > PNG > WebP > JPG > others)
 *   4. Same-host bonus (logos hosted on the prospect's domain are more likely
 *      to be official brand assets than CDN refs)
 */
export function rankLogoCandidates(urls: string[], homeUrl?: string): string[] {
  const homeHost = homeUrl ? new URL(homeUrl).hostname.replace(/^www\./, '') : null;
  const filtered = Array.from(new Set(urls.filter((u) => /^https?:/.test(u))));

  return filtered.sort((a, b) => {
    const extA = EXT_PRIORITY[inferExtension(a)] ?? 0;
    const extB = EXT_PRIORITY[inferExtension(b)] ?? 0;
    if (extA !== extB) return extB - extA;

    if (homeHost) {
      const aSameHost = new URL(a).hostname.replace(/^www\./, '') === homeHost;
      const bSameHost = new URL(b).hostname.replace(/^www\./, '') === homeHost;
      if (aSameHost !== bSameHost) return aSameHost ? -1 : 1;
    }
    return 0;
  });
}

export interface DownloadLogoOpts {
  homeUrl: string;
  outDir: string;
  /** Max width to downsize to (raster only). Default 512px. */
  maxWidth?: number;
}

export async function extractLogo(
  candidates: string[],
  opts: DownloadLogoOpts
): Promise<ExtractLogoResult> {
  const ranked = rankLogoCandidates(candidates, opts.homeUrl);
  if (ranked.length === 0) throw new Error('No usable logo candidates found');

  for (const url of ranked) {
    try {
      const res = await fetch(url);
      if (!res.ok) continue;
      const buf = Buffer.from(await res.arrayBuffer());
      const ext = inferExtension(url);

      if (ext === 'svg') {
        const filename = 'logo.svg';
        const fullPath = join(opts.outDir, filename);
        writeFileSync(fullPath, buf);
        return { filename, fullPath, processed: false };
      }

      // Raster: downsize via sharp if larger than maxWidth
      const maxWidth = opts.maxWidth ?? 512;
      const filename = `logo.${ext === 'jpg' ? 'jpeg' : ext}`;
      const fullPath = join(opts.outDir, filename);
      const meta = await sharp(buf).metadata();
      if ((meta.width ?? 0) > maxWidth) {
        await sharp(buf).resize({ width: maxWidth }).toFile(fullPath);
        return { filename, fullPath, processed: true };
      }
      writeFileSync(fullPath, buf);
      return { filename, fullPath, processed: false };
    } catch {
      continue; // try next candidate
    }
  }

  throw new Error(`All ${ranked.length} logo candidates failed to download`);
}
```

- [ ] **Step 4: Run tests, verify pass**

```bash
pnpm test scripts/theme-from-url/__tests__/extract-logo.test.ts
```

Expected: 8 tests pass.

- [ ] **Step 5: Wire into orchestrator**

In `scripts/theme-from-url.ts`, append after color extraction:

```typescript
const logo = await import('./theme-from-url/extract-logo').then((m) =>
  m.extractLogo(brand.logoCandidates, { homeUrl: brand.url, outDir: outPath })
);
console.log(`[theme-from-url] logo: ${logo.filename} (processed=${logo.processed})`);

// Tasks 6-7 will use brand.computedStyles + ai polish
throw new Error('Stages 4-5 not yet implemented — see Tasks 6-7');
```

Smoke test:

```bash
pnpm theme:from-url https://pedrollo.pl 2>&1 | head -20
ls -la themes/pedrollo/
```

Expected: `themes/pedrollo/logo.png` (or `logo.svg`) exists. File is reasonable size (~2-50KB).

- [ ] **Step 6: Commit**

```bash
git add scripts/theme-from-url/extract-logo.ts scripts/theme-from-url/__tests__/extract-logo.test.ts scripts/theme-from-url.ts
git commit -m "feat(crm): logo extraction with priority ranking + Sharp downsize"
```

---

## Task 6: Font detection + Google Fonts mapping

**Why:** Pull `font-family` from the homepage and try to map it to a Google Font that we can serve via Next's `next/font/google`. If no match, fall back to system fonts.

**Files:**
- Create: `scripts/theme-from-url/extract-fonts.ts`
- Create: `scripts/theme-from-url/__tests__/extract-fonts.test.ts`

- [ ] **Step 1: Write failing tests**

Create `scripts/theme-from-url/__tests__/extract-fonts.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { parseFontFamily, mapToGoogleFont } from '../extract-fonts';

describe('parseFontFamily', () => {
  it('extracts first font from font-family stack', () => {
    expect(parseFontFamily('"Helvetica Neue", Arial, sans-serif')).toBe('Helvetica Neue');
  });
  it('handles unquoted', () => {
    expect(parseFontFamily('Inter, sans-serif')).toBe('Inter');
  });
  it('handles single font', () => {
    expect(parseFontFamily('Roboto')).toBe('Roboto');
  });
  it('handles empty', () => {
    expect(parseFontFamily('')).toBe(null);
  });
  it('strips quotes from result', () => {
    expect(parseFontFamily(`"Open Sans", sans-serif`)).toBe('Open Sans');
    expect(parseFontFamily(`'Open Sans', sans-serif`)).toBe('Open Sans');
  });
});

describe('mapToGoogleFont', () => {
  it('maps common fonts', () => {
    expect(mapToGoogleFont('Roboto')).toBe('Roboto');
    expect(mapToGoogleFont('Inter')).toBe('Inter');
    expect(mapToGoogleFont('Open Sans')).toBe('Open Sans');
    expect(mapToGoogleFont('Montserrat')).toBe('Montserrat');
  });

  it('returns null for system fonts', () => {
    expect(mapToGoogleFont('Helvetica Neue')).toBe(null);
    expect(mapToGoogleFont('Arial')).toBe(null);
    expect(mapToGoogleFont('-apple-system')).toBe(null);
  });

  it('case-insensitive', () => {
    expect(mapToGoogleFont('roboto')).toBe('Roboto');
    expect(mapToGoogleFont('OPEN SANS')).toBe('Open Sans');
  });

  it('returns null for unknown fonts', () => {
    expect(mapToGoogleFont('SomeProprietaryFont')).toBe(null);
  });
});
```

- [ ] **Step 2: Verify fail**

```bash
pnpm test scripts/theme-from-url/__tests__/extract-fonts.test.ts
```

Expected: FAIL — module missing.

- [ ] **Step 3: Implement extract-fonts.ts**

Create `scripts/theme-from-url/extract-fonts.ts`:

```typescript
/**
 * Extract first concrete font name from a CSS font-family stack.
 * Returns null if string is empty or contains only generic families.
 */
export function parseFontFamily(input: string): string | null {
  if (!input) return null;
  const first = input.split(',')[0].trim();
  if (!first) return null;
  const cleaned = first.replace(/^["']|["']$/g, '').trim();
  if (!cleaned) return null;
  // Generic CSS family names — ignore
  if (['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui'].includes(cleaned.toLowerCase())) {
    return null;
  }
  return cleaned;
}

/**
 * Whitelist of popular Google Fonts (~30 most common). Case-insensitive lookup.
 * If a font isn't in this list, we assume it's not on Google Fonts and return null.
 */
const GOOGLE_FONTS: Record<string, string> = Object.fromEntries(
  [
    'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'Source Sans Pro', 'Source Sans 3',
    'Oswald', 'Raleway', 'Nunito', 'Nunito Sans', 'Poppins', 'Inter', 'Playfair Display',
    'Merriweather', 'PT Sans', 'PT Serif', 'Ubuntu', 'Roboto Slab', 'Roboto Mono',
    'Roboto Condensed', 'Bebas Neue', 'Quicksand', 'Cabin', 'Mukta', 'Rubik',
    'Work Sans', 'Karla', 'Manrope', 'Plus Jakarta Sans', 'DM Sans', 'DM Serif Display',
    'Space Grotesk', 'IBM Plex Sans', 'IBM Plex Serif', 'IBM Plex Mono', 'Fira Sans',
    'Fira Code',
  ].map((name) => [name.toLowerCase(), name])
);

export function mapToGoogleFont(name: string): string | null {
  if (!name) return null;
  const lower = name.toLowerCase();
  // Skip system font references
  if (lower.startsWith('-apple-') || lower.startsWith('-system-') || lower === 'system-ui') {
    return null;
  }
  return GOOGLE_FONTS[lower] ?? null;
}

export interface FontExtraction {
  /** Raw font-family value from heading element */
  rawHeading: string;
  /** Raw font-family value from body */
  rawBody: string;
  /** Best guess at heading font (Google Font name or null) */
  heading: string | null;
  /** Best guess at body font (Google Font name or null) */
  body: string | null;
}

export function extractFonts(computedStyles: {
  heading: { fontFamily: string };
  body: { fontFamily: string };
}): FontExtraction {
  const headingName = parseFontFamily(computedStyles.heading.fontFamily);
  const bodyName = parseFontFamily(computedStyles.body.fontFamily);
  return {
    rawHeading: computedStyles.heading.fontFamily,
    rawBody: computedStyles.body.fontFamily,
    heading: headingName ? mapToGoogleFont(headingName) : null,
    body: bodyName ? mapToGoogleFont(bodyName) : null,
  };
}
```

- [ ] **Step 4: Verify pass**

```bash
pnpm test scripts/theme-from-url/__tests__/extract-fonts.test.ts
```

Expected: 12 tests pass.

- [ ] **Step 5: Wire into orchestrator**

In `scripts/theme-from-url.ts`:

```typescript
const fonts = (await import('./theme-from-url/extract-fonts')).extractFonts(
  brand.computedStyles
);
console.log(`[theme-from-url] fonts: heading=${fonts.heading ?? '(system)'}, body=${fonts.body ?? '(system)'}`);

// Task 7 will pull AI polish + write final theme.json
throw new Error('Stage 5 not yet implemented — see Task 7');
```

- [ ] **Step 6: Commit**

```bash
git add scripts/theme-from-url/extract-fonts.ts scripts/theme-from-url/__tests__/extract-fonts.test.ts scripts/theme-from-url.ts
git commit -m "feat(crm): font detection + Google Fonts mapping"
```

---

## Task 7: AI polish (Claude Haiku) + theme.json writer

**Why:** Raw extraction is good but lossy — we get 6 brand colors but don't know which is `primary` vs `accent`, semantic mapping is missing, foregrounds are guessed. Claude Haiku takes the screenshot + extracted data and returns a polished structured palette.

**Files:**
- Create: `scripts/theme-from-url/ai-polish.ts`
- Modify: `scripts/theme-from-url.ts` (final orchestration: write `theme.json`)

- [ ] **Step 1: Implement ai-polish.ts**

Create `scripts/theme-from-url/ai-polish.ts`:

```typescript
import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';

const ANTHROPIC_KEY_PATH = process.env.ANTHROPIC_API_KEY ?? '';

const client = new Anthropic({ apiKey: ANTHROPIC_KEY_PATH });

const PolishedPaletteSchema = z.object({
  primary: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  primaryForeground: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  accent: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  accentForeground: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  background: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  foreground: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  sidebar: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  sidebarForeground: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  reasoning: z.string(),
});

export type PolishedPalette = z.infer<typeof PolishedPaletteSchema>;

export interface PolishOpts {
  /** Brand name (best guess from URL slug or fetched data) */
  brandName: string;
  /** Hex colors extracted by k-means */
  extractedColors: string[];
  /** PNG screenshot buffer */
  screenshot: Buffer;
}

export async function aiPolish(opts: PolishOpts): Promise<PolishedPalette> {
  if (!ANTHROPIC_KEY_PATH) {
    throw new Error(
      'ANTHROPIC_API_KEY not set — cannot run AI polish. Use --skip-ai to bypass.'
    );
  }

  const screenshotBase64 = opts.screenshot.toString('base64');

  const prompt = `You are a brand designer helping us build a CRM dashboard skinned in this brand's colors.

Brand: ${opts.brandName}
Extracted colors (k-means from homepage): ${opts.extractedColors.join(', ')}

Produce a structured palette for a CRM dashboard:
- primary: dominant brand color used for buttons, links, sidebar bg
- primaryForeground: text color readable on primary (usually white or near-white)
- accent: secondary brand color used for highlights, badges (different from primary)
- accentForeground: text color readable on accent
- background: page background (usually white or very light gray)
- foreground: main text color on background (usually near-black)
- sidebar: background color of left navigation (often = primary or a darker shade)
- sidebarForeground: text on sidebar

Use only colors from the extracted list OR very-near variations (we trust k-means). Keep WCAG AA contrast for foreground/background pairs.

Return ONLY valid JSON, no prose:
{
  "primary": "#...",
  "primaryForeground": "#...",
  "accent": "#...",
  "accentForeground": "#...",
  "background": "#...",
  "foreground": "#...",
  "sidebar": "#...",
  "sidebarForeground": "#...",
  "reasoning": "<one sentence explaining your choices>"
}`;

  const message = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 1024,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'image',
            source: {
              type: 'base64',
              media_type: 'image/png',
              data: screenshotBase64,
            },
          },
          { type: 'text', text: prompt },
        ],
      },
    ],
  });

  const textBlock = message.content.find((c) => c.type === 'text');
  if (!textBlock || textBlock.type !== 'text') {
    throw new Error('Claude returned no text');
  }

  // Extract JSON from response (Claude sometimes wraps in markdown)
  const jsonMatch = textBlock.text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) throw new Error(`No JSON in Claude response:\n${textBlock.text}`);

  const parsed = JSON.parse(jsonMatch[0]);
  const result = PolishedPaletteSchema.safeParse(parsed);
  if (!result.success) {
    throw new Error(
      `AI polish returned invalid shape:\n${result.error.errors.map((e) => `  ${e.path.join('.')}: ${e.message}`).join('\n')}`
    );
  }
  return result.data;
}

/**
 * Fallback when --skip-ai is passed: build palette mechanically from extracted colors.
 * Heuristic: first non-neutral = primary, second = accent. Neutrals are computed.
 */
export function fallbackPalette(opts: { brandName: string; extractedColors: string[] }): PolishedPalette {
  const [primary = '#0066cc', accent = '#ff6b35'] = opts.extractedColors;
  return {
    primary,
    primaryForeground: '#ffffff',
    accent,
    accentForeground: '#ffffff',
    background: '#ffffff',
    foreground: '#0a0a0a',
    sidebar: primary,
    sidebarForeground: '#ffffff',
    reasoning: 'fallback (--skip-ai): used first 2 extracted colors as primary/accent',
  };
}
```

- [ ] **Step 2: Wire AI polish + theme.json writer into orchestrator**

Replace the rest of `scripts/theme-from-url.ts` `buildTheme`:

```typescript
import { writeFileSync } from 'fs';
import { fetchBrand } from './theme-from-url/fetch-brand';
import { extractColors } from './theme-from-url/extract-colors';
import { extractLogo } from './theme-from-url/extract-logo';
import { extractFonts } from './theme-from-url/extract-fonts';
import { aiPolish, fallbackPalette } from './theme-from-url/ai-polish';

async function buildTheme(opts: BuildThemeOptions): Promise<void> {
  const slug = slugFromUrl(opts.url);
  const outPath = resolve(opts.outDir, slug);
  if (!existsSync(outPath)) mkdirSync(outPath, { recursive: true });
  console.log(`[theme-from-url] slug: ${slug}, output: ${outPath}`);

  const brand = await fetchBrand(opts.url, { verbose: opts.verbose });
  console.log(`[theme-from-url] fetched: ${brand.url}`);

  const colors = await extractColors(brand.homepageScreenshot, { maxColors: 6 });
  console.log(`[theme-from-url] colors: ${colors.map((c) => c.hex).join(', ')}`);

  const logo = await extractLogo(brand.logoCandidates, {
    homeUrl: brand.url,
    outDir: outPath,
  });
  console.log(`[theme-from-url] logo: ${logo.filename}`);

  const fonts = extractFonts(brand.computedStyles);
  console.log(
    `[theme-from-url] fonts: heading=${fonts.heading ?? '(system)'}, body=${fonts.body ?? '(system)'}`
  );

  const brandName = slug.charAt(0).toUpperCase() + slug.slice(1);
  const palette = opts.skipAi
    ? fallbackPalette({ brandName, extractedColors: colors.map((c) => c.hex) })
    : await aiPolish({ brandName, extractedColors: colors.map((c) => c.hex), screenshot: brand.homepageScreenshot });
  console.log(`[theme-from-url] palette ready: ${palette.reasoning}`);

  // Optional favicon
  let faviconRelPath = `/themes/${slug}/${logo.filename}`;
  if (brand.favicon) {
    try {
      const res = await fetch(brand.favicon);
      if (res.ok) {
        const ext = brand.favicon.match(/\.([a-z]{3,4})(?:\?|$)/i)?.[1] ?? 'ico';
        const fname = `favicon.${ext}`;
        writeFileSync(resolve(outPath, fname), Buffer.from(await res.arrayBuffer()));
        faviconRelPath = `/themes/${slug}/${fname}`;
      }
    } catch {
      /* fall through to logo as favicon */
    }
  }

  const themeJson = {
    brand: {
      name: brandName,
      logoUrl: `/themes/${slug}/${logo.filename}`,
      favicon: faviconRelPath,
    },
    colors: {
      primary: palette.primary,
      primaryForeground: palette.primaryForeground,
      accent: palette.accent,
      accentForeground: palette.accentForeground,
      background: palette.background,
      foreground: palette.foreground,
      sidebar: palette.sidebar,
      sidebarForeground: palette.sidebarForeground,
    },
    typography:
      fonts.heading || fonts.body
        ? {
            heading: fonts.heading ?? 'Plus Jakarta Sans',
            body: fonts.body ?? 'Plus Jakarta Sans',
          }
        : undefined,
    radius: '0.5rem',
    darkMode: false,
  };
  writeFileSync(resolve(outPath, 'theme.json'), JSON.stringify(themeJson, null, 2));
  console.log(`[theme-from-url] DONE — wrote ${outPath}/theme.json`);
}
```

- [ ] **Step 3: End-to-end smoke test (with API key)**

```bash
ANTHROPIC_API_KEY=$(cat ~/.config/anthropic_api_key 2>/dev/null) \
  pnpm theme:from-url https://pedrollo.pl 2>&1 | tail -10
```

If no `~/.config/anthropic_api_key` — set `ANTHROPIC_API_KEY` from your env. If you don't want to use AI:

```bash
pnpm theme:from-url --skip-ai https://pedrollo.pl
```

Expected: `themes/pedrollo/theme.json` + `themes/pedrollo/logo.png` (or .svg) + `themes/pedrollo/favicon.ico`. Inspect:

```bash
cat themes/pedrollo/theme.json | jq
```

Expected: valid JSON matching the Theme schema from `src/lib/theme.ts`. Should be loadable:

```bash
DATABASE_URL=postgresql://test/test pnpm exec tsx -e "import { loadTheme } from './src/lib/theme'; console.log(loadTheme('./themes/pedrollo/theme.json'))"
```

Expected: prints parsed Theme object — no Zod errors.

- [ ] **Step 4: Cleanup test theme**

```bash
rm -rf themes/pedrollo
```

(We'll regenerate properly via `/crm-new-demo` skill in Task 13.)

- [ ] **Step 5: Commit**

```bash
git add scripts/theme-from-url/ai-polish.ts scripts/theme-from-url.ts
git commit -m "feat(crm): AI polish + theme.json writer — full theme-from-url pipeline"
```

---

## Task 8: Tweak preview tool

**Why:** Even after AI polish, sometimes Kacper wants to manually swap one color before the demo. A tiny preview server shows a sample CRM dashboard with the theme applied + inline color pickers; he clicks, swaps, saves.

**Files:**
- Create: `scripts/theme-tweak.ts` (Express + minimal HTML)
- Modify: `package.json` — add `theme:tweak` script + express dep (already added in Task 2 if pre-installed, else now)

- [ ] **Step 1: Verify express is in deps**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
grep '"express"' package.json
```

If absent: `pnpm add express @types/express`.

- [ ] **Step 2: Implement scripts/theme-tweak.ts**

Create `scripts/theme-tweak.ts`:

```typescript
#!/usr/bin/env tsx
import { Command } from 'commander';
import { resolve } from 'path';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import express from 'express';
import { parseTheme, themeToCssVars, type Theme } from '@/lib/theme';

const PORT = 3099;

function htmlPage(theme: Theme, slug: string): string {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Theme tweak — ${slug}</title>
<style>
  :root { ${themeToCssVars(theme)} }
  body { margin: 0; font-family: ${theme.typography?.body ?? 'system-ui'}, sans-serif; background: var(--color-background); color: var(--color-foreground); }
  .layout { display: grid; grid-template-columns: 220px 1fr; min-height: 100vh; }
  .sidebar { background: var(--color-sidebar); color: var(--color-sidebar-foreground); padding: 24px; }
  .sidebar h2 { margin-top: 0; font-family: ${theme.typography?.heading ?? 'system-ui'}, sans-serif; }
  .sidebar a { display: block; padding: 8px 0; color: inherit; text-decoration: none; opacity: 0.8; }
  .main { padding: 32px; }
  .card { background: white; border-radius: var(--radius); padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 24px; }
  .button { background: var(--color-primary); color: var(--color-primary-foreground); padding: 10px 20px; border: none; border-radius: var(--radius); cursor: pointer; font-weight: 600; }
  .badge { background: var(--color-accent); color: var(--color-accent-foreground); padding: 4px 10px; border-radius: 999px; font-size: 12px; display: inline-block; }
  .swatch-row { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 24px; }
  .swatch { display: flex; flex-direction: column; gap: 4px; }
  .swatch input[type=color] { width: 60px; height: 60px; border: 1px solid #ccc; border-radius: 8px; cursor: pointer; padding: 0; }
  .swatch label { font-size: 11px; color: #666; }
  .actions { margin-top: 32px; display: flex; gap: 12px; }
  .actions button { padding: 10px 20px; border-radius: 6px; border: 1px solid #ccc; background: white; cursor: pointer; font-weight: 600; }
  .actions button.primary { background: var(--color-primary); color: var(--color-primary-foreground); border-color: var(--color-primary); }
</style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h2>${theme.brand.name}</h2>
      <a>📊 Sales</a>
      <a>📣 Marketing</a>
      <a>⚙ Operations</a>
      <a>👥 Baza</a>
    </aside>
    <main class="main">
      <h1>Theme preview — <code>${slug}</code></h1>
      <p>Klikaj kolory poniżej, żeby zmienić paletę. Po akceptacji kliknij „Save & exit".</p>

      <div class="card">
        <h3>Sample deal card</h3>
        <p>Acme sp. z o.o. — Wycena <span class="badge">Hot</span></p>
        <button class="button">Otwórz deal</button>
      </div>

      <h3>Edytuj paletę</h3>
      <div class="swatch-row">
        ${(['primary', 'primaryForeground', 'accent', 'accentForeground', 'background', 'foreground', 'sidebar', 'sidebarForeground'] as const)
          .map(
            (key) => `
          <div class="swatch">
            <input type="color" data-key="${key}" value="${theme.colors[key]}" />
            <label>${key}</label>
          </div>`
          )
          .join('')}
      </div>

      <div class="actions">
        <button class="primary" id="save">Save & exit</button>
        <button id="reset">Reset</button>
      </div>
    </main>
  </div>

<script>
  const initialColors = ${JSON.stringify(theme.colors)};
  const inputs = document.querySelectorAll('input[type=color]');
  inputs.forEach(input => input.addEventListener('input', () => {
    const key = input.dataset.key;
    document.documentElement.style.setProperty('--color-' + key.replace(/([A-Z])/g, '-$1').toLowerCase(), input.value);
  }));
  document.getElementById('reset').onclick = () => {
    inputs.forEach(input => {
      input.value = initialColors[input.dataset.key];
      input.dispatchEvent(new Event('input'));
    });
  };
  document.getElementById('save').onclick = async () => {
    const colors = {};
    inputs.forEach(input => { colors[input.dataset.key] = input.value; });
    const res = await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ colors }) });
    if (res.ok) {
      document.body.innerHTML = '<h1 style="text-align:center; margin-top:30vh;">Saved. You can close this tab.</h1>';
      setTimeout(() => window.close(), 800);
    } else {
      alert('Save failed: ' + (await res.text()));
    }
  };
</script>
</body>
</html>`;
}

async function main() {
  const program = new Command();
  program
    .argument('<slug>', 'theme slug (folder under themes/)')
    .option('-d, --themes-dir <dir>', 'themes root', './themes')
    .action(async (slug, options) => {
      const themePath = resolve(options.themesDir, slug, 'theme.json');
      if (!existsSync(themePath)) {
        console.error(`No theme.json at ${themePath}`);
        process.exit(1);
      }
      let theme = parseTheme(JSON.parse(readFileSync(themePath, 'utf-8')));

      const app = express();
      app.use(express.json());
      app.get('/', (_req, res) => res.send(htmlPage(theme, slug)));
      app.post('/save', (req, res) => {
        const colorsUpdate = req.body?.colors;
        if (!colorsUpdate) return res.status(400).send('missing colors');
        try {
          theme = parseTheme({ ...theme, colors: colorsUpdate });
          writeFileSync(themePath, JSON.stringify(theme, null, 2));
          res.send('ok');
          setTimeout(() => process.exit(0), 200);
        } catch (err) {
          res.status(400).send(err instanceof Error ? err.message : 'invalid');
        }
      });

      app.listen(PORT, () => {
        const url = `http://localhost:${PORT}`;
        console.log(`[theme-tweak] preview at ${url} — opening browser...`);
        // Best-effort open (mac/linux/windows)
        const opener =
          process.platform === 'darwin'
            ? 'open'
            : process.platform === 'win32'
            ? 'start'
            : 'xdg-open';
        import('child_process').then((cp) =>
          cp.exec(`${opener} ${url}`, () => {
            /* ignore */
          })
        );
      });
    });

  await program.parseAsync();
}

main();
```

- [ ] **Step 3: Add `theme:tweak` script**

In `package.json` `scripts`:

```json
"theme:tweak": "tsx scripts/theme-tweak.ts"
```

- [ ] **Step 4: Smoke test (manual)**

```bash
# Make sure themes/default/theme.json exists from Plan 1; if not, copy it from main
pnpm theme:tweak default
```

Expected: browser opens at `http://localhost:3099`, shows sample dashboard with Dokodu colors, color pickers work, "Save & exit" persists changes back to `themes/default/theme.json`.

Test save:
- Click any swatch, pick a different color
- Click "Save & exit" → server exits, page says "Saved"
- Verify: `cat themes/default/theme.json` shows the new color
- Restore: `git checkout themes/default/theme.json`

- [ ] **Step 5: Commit**

```bash
git add scripts/theme-tweak.ts package.json pnpm-lock.yaml
git commit -m "feat(crm): theme-tweak preview server with color pickers"
```

---

## Task 9: Reverse-nginx route config

**Why:** Each instance lives at `dev.dokodu.it/crm-{slug}/`. The Dokodu reverse-nginx (Docker container in `/srv/reverse-proxy/`) needs a single config that pattern-matches `/crm-*` paths and proxies to the right container on the `web` Docker network.

**Files (server-side):**
- Create on server: `/srv/reverse-proxy/conf.d/crm-instances.conf`

- [ ] **Step 1: Verify SSH access to server**

```bash
ssh deploy@57.128.219.9 "ls /srv/reverse-proxy/conf.d/"
```

Expected: directory listing of existing nginx conf.d files. If permission denied, request access from Kacper.

- [ ] **Step 2: Inspect existing dev.dokodu.it server block**

```bash
ssh deploy@57.128.219.9 "cat /srv/reverse-proxy/conf.d/*.conf | grep -A 30 'dev.dokodu.it' | head -60"
```

Expected: existing server block(s) for `dev.dokodu.it`. Note SSL setup, port (80/443), upstream patterns. Goal: our new config must NOT collide with existing locations.

- [ ] **Step 3: Create the crm-instances.conf locally first (for review)**

Create file `/tmp/crm-instances.conf`:

```nginx
# /srv/reverse-proxy/conf.d/crm-instances.conf
#
# Routes for Dokodu CRM multi-instance demos at dev.dokodu.it/crm-{slug}/
# Plan 2 — see ~/DOKODU_BRAIN/docs/superpowers/plans/2026-04-28-crm-theme-deploy-pedrollo.md
#
# Each prospect's container is named `crm-{slug}` and listens on port 3001
# inside the `web` Docker network. We use a regex location to dynamically
# proxy /crm-{slug}/... → http://crm-{slug}:3001/crm-{slug}/...
#
# Master demo (no slug) lives at /crm/ and is handled by `crm-master`.

server {
    listen 80;
    listen 443 ssl http2;
    server_name dev.dokodu.it;

    ssl_certificate     /etc/letsencrypt/live/dokodu.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dokodu.it/privkey.pem;

    # Increase body size for file uploads (attachments)
    client_max_body_size 50M;

    # Per-instance routing: /crm-{slug}/... → crm-{slug} container
    # The captured slug is used both for upstream selection AND for the
    # X-Forwarded-Prefix header (Next.js basePath was baked in at build,
    # but downstream services may want the prefix info too).
    location ~ ^/crm-(?<slug>[a-z0-9-]+)(/.*)?$ {
        # Resolve container name dynamically — Docker DNS handles this on `web` network
        resolver 127.0.0.11 valid=10s;
        set $upstream_host crm-$slug;
        proxy_pass http://$upstream_host:3001$request_uri;

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Prefix /crm-$slug;
        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";

        # Reasonable timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout    60s;
        proxy_read_timeout    60s;

        # If the container is down, return 502 fast instead of hanging
        proxy_next_upstream error timeout invalid_header http_502 http_503 http_504;
    }

    # Master demo at /crm/
    location /crm/ {
        resolver 127.0.0.11 valid=10s;
        set $upstream_host crm-master;
        proxy_pass http://$upstream_host:3001$request_uri;

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";
    }
}
```

Review the config inline. Verify it doesn't conflict with existing `dev.dokodu.it` server blocks (Step 2). If a `dev.dokodu.it` block already exists, this config replaces or merges with it — note which.

If existing config has other locations (e.g., `/grafana/`, `/sentry/`), those need to live in this new file too OR the existing config must remain and this file uses different `server_name` matching technique. **Do not deploy until this is verified.**

- [ ] **Step 4: Deploy config to server (idempotent)**

```bash
scp /tmp/crm-instances.conf deploy@57.128.219.9:/tmp/crm-instances.conf
ssh deploy@57.128.219.9 "
  set -e
  sudo mv /tmp/crm-instances.conf /srv/reverse-proxy/conf.d/crm-instances.conf
  cd /srv/reverse-proxy
  docker compose exec reverse-nginx nginx -t
  docker compose exec reverse-nginx nginx -s reload
"
```

Expected: `nginx -t` reports `syntax is ok` and `test is successful`. `nginx -s reload` reports nothing (silent success).

If nginx -t fails: do NOT reload. Read error, fix locally, re-deploy.

- [ ] **Step 5: Smoke test routing (with NO instance running yet)**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://dev.dokodu.it/crm-nonexistent/
```

Expected: `502` (bad gateway — nginx can't resolve `crm-nonexistent`). This means routing works; the missing instance is the expected failure.

If you get `404` — nginx config didn't load. Check `nginx -t` and reload again.

- [ ] **Step 6: Cleanup local file**

```bash
rm /tmp/crm-instances.conf
```

- [ ] **Step 7: Commit reference copy locally (so Plan 2 history records what was deployed)**

```bash
mkdir -p /Users/ksieradzinski/Projects/dokodu/crm-new/deploy/nginx
cd /Users/ksieradzinski/Projects/dokodu/crm-new
cp deploy/nginx/crm-instances.conf.template -f 2>/dev/null || true
# Recreate the file at deploy/nginx/crm-instances.conf for source-of-truth
```

Write `deploy/nginx/crm-instances.conf` with the same content as in Step 3 (this is the canonical template; Task 10's deploy script ensures the server matches).

```bash
git add deploy/nginx/crm-instances.conf
git commit -m "feat(crm): reverse-nginx config for /crm-{slug} path routing"
```

---

## Task 10: Deploy script (`scripts/deploy-instance.sh`)

**Why:** End-to-end automation of "given a slug + theme, bring up a working containerized demo on the Dokodu server." Used by the BRAIN skill in Task 13.

**Files:**
- Create: `scripts/deploy-instance.sh`
- Create: `scripts/destroy-instance.sh`
- Create: `scripts/list-instances.sh`

- [ ] **Step 1: Implement deploy-instance.sh**

Create `scripts/deploy-instance.sh` (chmod +x):

```bash
#!/usr/bin/env bash
set -euo pipefail

# scripts/deploy-instance.sh
#
# Usage: deploy-instance.sh <slug> [--bundle <name>]
# Example: deploy-instance.sh pedrollo --bundle distribution-b2b
#
# Requirements:
#   - themes/<slug>/theme.json exists locally (created by /crm-new-demo skill)
#   - SSH access to deploy@57.128.219.9
#   - Docker buildx with --build-arg support
#
# What it does (idempotent — safe to re-run):
#   1. Generate compose-<slug>.yml from docker-compose.template.yml
#   2. Copy theme files to server
#   3. Build image on server with BUILD_BASE_PATH=/crm-<slug>
#   4. Run prisma migrations + seed bundle in migrate container
#   5. Start crm-<slug> + crm-db-<slug>
#   6. Wait for /api/health to return 200
#   7. Print final URL

SLUG="${1:-}"
BUNDLE="${2:---bundle}"
BUNDLE_NAME="${3:-}"

if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <slug> [--bundle <name>]" >&2
  exit 2
fi

SERVER="deploy@57.128.219.9"
REMOTE_BASE="/home/deploy/crm-instances/$SLUG"
LOCAL_THEME_DIR="./themes/$SLUG"

if [[ ! -f "$LOCAL_THEME_DIR/theme.json" ]]; then
  echo "ERROR: No theme.json at $LOCAL_THEME_DIR/theme.json" >&2
  echo "Run: pnpm theme:from-url https://example.com" >&2
  exit 1
fi

echo "[deploy] slug=$SLUG bundle=${BUNDLE_NAME:-(none)}"

# Generate random secrets per-instance (only if not already present on server)
DB_PASSWORD="$(openssl rand -hex 16)"
NEXTAUTH_SECRET="$(openssl rand -hex 32)"

# Step 1: prepare remote dir + transfer theme + generate compose
echo "[deploy] preparing remote dir + transferring theme"
ssh "$SERVER" "mkdir -p $REMOTE_BASE/themes/$SLUG"
rsync -az "$LOCAL_THEME_DIR/" "$SERVER:$REMOTE_BASE/themes/$SLUG/"
rsync -az ./docker-compose.template.yml "$SERVER:$REMOTE_BASE/"

# Step 2: build the docker-compose file from template via envsubst
ssh "$SERVER" "
  set -euo pipefail
  cd $REMOTE_BASE
  if [[ ! -f .env ]]; then
    cat > .env <<EOF
SLUG=$SLUG
BASE_PATH=/crm-$SLUG
THEME_PATH=./themes/$SLUG/theme.json
MODULES_ENABLED=
DB_PASSWORD=$DB_PASSWORD
NEXTAUTH_SECRET=$NEXTAUTH_SECRET
NEXTAUTH_URL=https://dev.dokodu.it/crm-$SLUG
EOF
    chmod 600 .env
  fi
  set -a; . ./.env; set +a
  envsubst < docker-compose.template.yml > docker-compose.${SLUG}.yml
"

# Step 3: build image (we transfer the whole repo via rsync to /tmp/crm-build,
# build there with --build-arg BUILD_BASE_PATH, then docker compose uses
# the resulting tag). For simplicity we build in-place where the compose file lives;
# this means the server needs the source. Alternative: build locally + push to
# a local registry — but Plan 2 prefers simplicity over pre-baked registry.

echo "[deploy] syncing source to server build dir"
ssh "$SERVER" "mkdir -p $REMOTE_BASE/build"
rsync -az --delete \
  --exclude='node_modules' --exclude='.next' --exclude='.git' \
  --exclude='__tests__' --exclude='*.test.ts' --exclude='vitest.config.ts' \
  --exclude='vitest.setup.ts' --exclude='docs' \
  ./ "$SERVER:$REMOTE_BASE/build/"

# Also include the slug-specific theme inside the build context so it's available
# at COPY . . time
rsync -az "$LOCAL_THEME_DIR/" "$SERVER:$REMOTE_BASE/build/themes/$SLUG/"

echo "[deploy] building image"
ssh "$SERVER" "
  set -euo pipefail
  cd $REMOTE_BASE/build
  docker build --build-arg BUILD_BASE_PATH=/crm-$SLUG -t dokodu-crm:$SLUG .
"

# Step 4: run migrations + seed
echo "[deploy] running migrations + seed"
ssh "$SERVER" "
  set -euo pipefail
  cd $REMOTE_BASE
  docker compose -f docker-compose.${SLUG}.yml -p crm-${SLUG} --profile migrate run --rm crm-migrate-${SLUG}
"

# If a bundle was specified, run it
if [[ -n "$BUNDLE_NAME" && "$BUNDLE" == "--bundle" ]]; then
  echo "[deploy] applying seed bundle: $BUNDLE_NAME"
  ssh "$SERVER" "
    set -euo pipefail
    cd $REMOTE_BASE
    docker compose -f docker-compose.${SLUG}.yml -p crm-${SLUG} \
      run --rm \
      -e SEED_BUNDLE=$BUNDLE_NAME \
      crm-migrate-${SLUG} \
      sh -c 'npx tsx /app/seed-bundles/_lib/load-bundle.ts'
  "
fi

# Step 5: start application containers
echo "[deploy] starting crm-$SLUG"
ssh "$SERVER" "
  set -euo pipefail
  cd $REMOTE_BASE
  docker compose -f docker-compose.${SLUG}.yml -p crm-${SLUG} up -d crm crm-db-${SLUG}
"

# Step 6: wait for healthcheck
echo "[deploy] waiting for /api/health..."
URL="https://dev.dokodu.it/crm-$SLUG/api/health"
for i in {1..30}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  if [[ "$STATUS" == "200" ]]; then
    echo "[deploy] HEALTHY after $((i * 2))s"
    break
  fi
  echo "  attempt $i: $STATUS"
  sleep 2
done

if [[ "$STATUS" != "200" ]]; then
  echo "[deploy] FAILED — final status: $STATUS"
  echo "Check logs: ssh $SERVER 'cd $REMOTE_BASE && docker compose -f docker-compose.${SLUG}.yml logs --tail 50'"
  exit 1
fi

echo
echo "[deploy] ✅ DONE"
echo "URL: https://dev.dokodu.it/crm-$SLUG"
```

- [ ] **Step 2: Implement destroy-instance.sh**

```bash
#!/usr/bin/env bash
set -euo pipefail

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <slug>" >&2
  exit 2
fi

SERVER="deploy@57.128.219.9"
REMOTE_BASE="/home/deploy/crm-instances/$SLUG"

echo "[destroy] tearing down crm-$SLUG"
ssh "$SERVER" "
  set -euo pipefail
  cd $REMOTE_BASE
  docker compose -f docker-compose.${SLUG}.yml -p crm-${SLUG} down -v
  cd ..
  rm -rf $SLUG
"
echo "[destroy] DONE — crm-$SLUG removed (containers, volumes, theme)"
```

- [ ] **Step 3: Implement list-instances.sh**

```bash
#!/usr/bin/env bash
set -euo pipefail

SERVER="deploy@57.128.219.9"

ssh "$SERVER" "docker ps --filter 'label=dokodu.crm.instance=true' --format 'json'" \
  | jq -s 'map({slug: .Labels | capture(\"dokodu.crm.slug=(?<s>[a-z0-9-]+)\").s, name: .Names, status: .Status, image: .Image})'
```

- [ ] **Step 4: Make scripts executable**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
chmod +x scripts/deploy-instance.sh scripts/destroy-instance.sh scripts/list-instances.sh
```

- [ ] **Step 5: Commit**

```bash
git add scripts/deploy-instance.sh scripts/destroy-instance.sh scripts/list-instances.sh
git commit -m "feat(crm): deploy/destroy/list instance scripts"
```

(End-to-end smoke test of these scripts happens in Task 15.)

---

## Task 11: Seed bundle infrastructure

**Why:** Each industry has different default pipeline stages, contact roles, deal templates. We separate generic seed (admin user, default permissions) from industry-specific seed (companies, contacts, products, deals).

**Files:**
- Create: `seed-bundles/_lib/factories.ts` (typed factory functions)
- Create: `seed-bundles/_lib/load-bundle.ts` (dispatcher)
- Modify: `prisma/seed.ts` (call dispatcher when SEED_BUNDLE env is set)

- [ ] **Step 1: Implement factories.ts**

Create `seed-bundles/_lib/factories.ts`:

```typescript
import { PrismaClient, type Prisma } from '@prisma/client';

/**
 * Typed factory helpers for seed bundles. Each factory returns a partial
 * record with the fields most commonly randomized; the bundle's seed.ts
 * supplies overrides for what matters per industry.
 */

let counter = 0;
const next = () => `seed-${++counter}`;

export function company(prisma: PrismaClient, overrides: Partial<Prisma.CompanyUncheckedCreateInput> = {}) {
  return prisma.company.create({
    data: {
      name: `Sample Company ${next()}`,
      industry: 'OTHER',
      size: 'SMALL',
      source: 'MANUAL',
      status: 'PROSPECT',
      ...overrides,
    },
  });
}

export function contact(
  prisma: PrismaClient,
  companyId: string,
  overrides: Partial<Prisma.ContactPersonUncheckedCreateInput> = {}
) {
  return prisma.contactPerson.create({
    data: {
      firstName: 'Anna',
      lastName: 'Nowak',
      email: `${next()}@example.com`,
      companyId,
      isPrimary: true,
      ...overrides,
    },
  });
}

export async function deal(
  prisma: PrismaClient,
  args: {
    title: string;
    companyId: string;
    pipelineId: string;
    stageId: string;
    assignedToId: string;
    value?: number;
    serviceType?: Prisma.DealUncheckedCreateInput['serviceType'];
  } & Partial<Prisma.DealUncheckedCreateInput>
) {
  return prisma.deal.create({
    data: {
      currency: 'PLN',
      dealType: 'NEW_BUSINESS',
      ...args,
    },
  });
}

export function activity(
  prisma: PrismaClient,
  args: {
    type: Prisma.ActivityUncheckedCreateInput['type'];
    subject: string;
    happenedAt: Date;
    userId: string;
    dealId?: string;
    companyId?: string;
  } & Partial<Prisma.ActivityUncheckedCreateInput>
) {
  return prisma.activity.create({ data: args });
}

export function task(
  prisma: PrismaClient,
  args: {
    title: string;
    priority: Prisma.TaskUncheckedCreateInput['priority'];
    type: Prisma.TaskUncheckedCreateInput['type'];
    assignedToId: string;
    createdById: string;
  } & Partial<Prisma.TaskUncheckedCreateInput>
) {
  return prisma.task.create({ data: args });
}

export interface BundleContext {
  prisma: PrismaClient;
  /** ID of the seeded admin user */
  adminUserId: string;
  /** ID of the default pipeline */
  pipelineId: string;
  /** Map of stage name → stage ID for the default pipeline */
  stageMap: Record<string, string>;
}

export interface SeedBundle {
  name: string;
  description: string;
  seed: (ctx: BundleContext) => Promise<void>;
}
```

- [ ] **Step 2: Implement load-bundle.ts dispatcher**

Create `seed-bundles/_lib/load-bundle.ts`:

```typescript
#!/usr/bin/env tsx
import { PrismaClient } from '@prisma/client';
import type { SeedBundle, BundleContext } from './factories';

const prisma = new PrismaClient();

async function main() {
  const bundleName = process.env.SEED_BUNDLE;
  if (!bundleName) {
    console.error('SEED_BUNDLE env var is required');
    process.exit(1);
  }

  // Dynamic import — bundle file at seed-bundles/{name}/seed.ts
  const mod = (await import(`../${bundleName}/seed`)) as { default: SeedBundle };
  const bundle = mod.default;
  if (!bundle?.seed) {
    console.error(`Bundle ${bundleName} has no default export with .seed`);
    process.exit(1);
  }

  console.log(`[load-bundle] ${bundle.name}: ${bundle.description}`);

  // Discover required IDs
  const adminUser = await prisma.user.findFirst({
    where: { roles: { some: { role: { name: 'admin' } } } },
  });
  if (!adminUser) throw new Error('No admin user found — run prisma db seed first');

  const pipeline = await prisma.pipeline.findFirst({
    where: { isDefault: true },
    include: { stages: true },
  });
  if (!pipeline) throw new Error('No default pipeline — run prisma db seed first');

  const stageMap = Object.fromEntries(pipeline.stages.map((s) => [s.name, s.id]));

  const ctx: BundleContext = {
    prisma,
    adminUserId: adminUser.id,
    pipelineId: pipeline.id,
    stageMap,
  };

  await bundle.seed(ctx);
  console.log(`[load-bundle] ${bundleName} applied successfully`);
  await prisma.$disconnect();
}

main().catch((err) => {
  console.error(err);
  prisma.$disconnect();
  process.exit(1);
});
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm exec tsc --noEmit
```

Expected: no NEW errors. Pre-existing errors in other files OK.

- [ ] **Step 4: Commit**

```bash
git add seed-bundles/_lib/
git commit -m "feat(crm): seed bundle infrastructure (factories + dispatcher)"
```

---

## Task 12: Pedrollo seed bundle (distribution-b2b)

**Why:** First real seed bundle — gives a freshly deployed `/crm-pedrollo` instance ~10 sample companies, contacts, deals, and activities so the demo doesn't feel empty. Industry-appropriate content (instalatorzy, dystrybutorzy, projektanci instalacji wodnych).

**Files:**
- Create: `seed-bundles/distribution-b2b/seed.ts`
- Create: `seed-bundles/distribution-b2b/README.md`

- [ ] **Step 1: Implement seed.ts**

Create `seed-bundles/distribution-b2b/seed.ts`:

```typescript
import type { SeedBundle, BundleContext } from '../_lib/factories';
import { company, contact, deal, activity } from '../_lib/factories';

const sampleCompanies = [
  { name: 'Hydro-Tech Instalacje sp. z o.o.', industry: 'CONSTRUCTION', size: 'SMALL' as const, city: 'Warszawa' },
  { name: 'Aquatech Hurtownia Wodno-Kanalizacyjna', industry: 'WHOLESALE', size: 'MEDIUM' as const, city: 'Kraków' },
  { name: 'Projekt-WOD Biuro Projektowe', industry: 'ENGINEERING', size: 'SMALL' as const, city: 'Wrocław' },
  { name: 'Aquaserwis sp. z o.o.', industry: 'CONSTRUCTION', size: 'SMALL' as const, city: 'Poznań' },
  { name: 'WaterFlow Inwestycje', industry: 'REAL_ESTATE', size: 'MEDIUM' as const, city: 'Gdańsk' },
  { name: 'Hurtownia HydroMag', industry: 'WHOLESALE', size: 'MEDIUM' as const, city: 'Łódź' },
  { name: 'TechFlow Instalacje', industry: 'CONSTRUCTION', size: 'MICRO' as const, city: 'Katowice' },
  { name: 'Pompy & Systemy', industry: 'WHOLESALE', size: 'LARGE' as const, city: 'Warszawa' },
];

const sampleContacts = [
  { first: 'Marek', last: 'Kowalski', position: 'Kierownik zakupów', email: 'marek.kowalski@', role: 'DECISION_MAKER' as const },
  { first: 'Anna', last: 'Nowak', position: 'Główna księgowa', email: 'anna.nowak@', role: 'INFLUENCER' as const },
  { first: 'Piotr', last: 'Wiśniewski', position: 'Instalator', email: 'piotr.w@', role: 'USER' as const },
  { first: 'Katarzyna', last: 'Zielińska', position: 'Projektant', email: 'k.zielinska@', role: 'CHAMPION' as const },
];

const stageProgression = ['Lead', 'Wycena', 'Negocjacje', 'Won', 'Lost']; // expected pipeline stages

const bundle: SeedBundle = {
  name: 'distribution-b2b',
  description: 'Sample data for B2B distribution / wholesale (Pedrollo, HABA, etc.)',
  seed: async (ctx: BundleContext) => {
    const { prisma, adminUserId, pipelineId, stageMap } = ctx;

    for (const stage of stageProgression) {
      if (!stageMap[stage]) {
        throw new Error(
          `Pipeline missing stage "${stage}". Expected default stages: ${stageProgression.join(', ')}`
        );
      }
    }

    for (let i = 0; i < sampleCompanies.length; i++) {
      const c = sampleCompanies[i];
      const company1 = await company(prisma, {
        ...c,
        source: 'MANUAL',
        status: i < 3 ? 'CLIENT' : 'PROSPECT',
        assignedToId: adminUserId,
      });

      // 1-2 contacts per company
      const numContacts = i < 4 ? 2 : 1;
      const contactIds: string[] = [];
      for (let j = 0; j < numContacts; j++) {
        const t = sampleContacts[(i + j) % sampleContacts.length];
        const created = await contact(prisma, company1.id, {
          firstName: t.first,
          lastName: t.last,
          position: t.position,
          email: `${t.email}${company1.name.toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 12)}.pl`,
          roleType: t.role,
          isPrimary: j === 0,
        });
        contactIds.push(created.id);
      }

      // Distribute across pipeline stages: 4 won, 1 lost, 3 in progress
      const stageIdx = i < 3 ? 3 : i === 3 ? 4 : (i % 3);
      const stageName = stageProgression[stageIdx];
      const stageId = stageMap[stageName];
      const value = 10000 + (i * 4500);

      const dealRec = await deal(prisma, {
        title: `Zamówienie pomp dla ${c.name.split(' ')[0]}`,
        companyId: company1.id,
        pipelineId,
        stageId,
        assignedToId: adminUserId,
        value,
        serviceType: 'OTHER',
        ...(stageName === 'Won' ? { wonDate: new Date(Date.now() - i * 86400000 * 30) } : {}),
        ...(stageName === 'Lost' ? { lostDate: new Date(Date.now() - 14 * 86400000), lostReasonCategory: 'PRICE' } : {}),
      });

      // Activities (1-3 per deal, depending on stage)
      const numActivities = stageIdx === 0 ? 1 : stageIdx >= 3 ? 3 : 2;
      for (let k = 0; k < numActivities; k++) {
        await activity(prisma, {
          type: k === 0 ? 'EMAIL_SENT' : k === 1 ? 'CALL' : 'MEETING',
          subject: k === 0 ? 'Wstępne zapytanie o ofertę' : k === 1 ? 'Telefon — uściślenie wymagań' : 'Spotkanie online',
          happenedAt: new Date(Date.now() - (numActivities - k) * 5 * 86400000),
          userId: adminUserId,
          dealId: dealRec.id,
          companyId: company1.id,
        });
      }
    }
  },
};

export default bundle;
```

- [ ] **Step 2: Implement README.md**

Create `seed-bundles/distribution-b2b/README.md`:

```markdown
# distribution-b2b seed bundle

**Use for**: B2B distribution / wholesale clients (e.g. Pedrollo for pumps, HABA for water treatment systems, dystrybutorzy materiałów budowlanych).

## What's seeded

- 8 sample companies in construction / wholesale / engineering / real estate
- 12-16 contacts (mix of decision makers, influencers, champions, users)
- 8 deals across pipeline stages (3 Won, 1 Lost, 4 in-progress)
- 16-24 activities (emails, calls, meetings)

## Why these names

Names are realistic Polish company names from the wodno-kanalizacyjna /
hydrauliczna industry. They're fictional but plausible — avoid using real
competitor names.

## Customizing per prospect

After deploy, manually edit company names in Prisma Studio if a more
prospect-specific touch is desired (e.g., for Pedrollo demo, change
"Hydro-Tech Instalacje" to a real distributor of Pedrollo pumps).

## Required pipeline stages

`Lead` / `Wycena` / `Negocjacje` / `Won` / `Lost`. These should match the
default pipeline created by `prisma/seed.ts`. If your default pipeline uses
different names, edit the `stageProgression` array in seed.ts.
```

- [ ] **Step 3: Verify the bundle compiles + dispatcher loads it**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm exec tsc --noEmit
```

Expected: no NEW errors.

(End-to-end test happens in Task 15 with full deploy.)

- [ ] **Step 4: Commit**

```bash
git add seed-bundles/distribution-b2b/
git commit -m "feat(crm): distribution-b2b seed bundle (Pedrollo + similar)"
```

---

## Task 13: BRAIN skill `/crm-new-demo`

**Why:** End-user-facing orchestrator. Kacper types `/crm-new-demo pedrollo.pl` and within 5 minutes has a working themed CRM at `dev.dokodu.it/crm-pedrollo`.

**Files:**
- Create: `~/Projects/dokodu/brain-public/.claude/skills/crm-new-demo/SKILL.md`

- [ ] **Step 1: Write the skill**

Create the file with this content:

````markdown
---
name: crm-new-demo
description: Tworzy nową instancję demo CRM dla prospektu — pobiera brand z URL klienta (Playwright + AI palette), buduje image, deployuje na dev.dokodu.it/crm-{slug}, ładuje seed danych branżowych. Trigger: "stwórz demo crm dla", "nowa instancja crm", "demo dla pedrollo", "/crm-new-demo {url}".
---

# Instrukcja: CRM New Demo

## Działanie

End-to-end deployment nowej instancji CRM dla prospektu Dokodu. Pipeline:
1. Pobranie brandu z URL prospektu (Playwright fetcher + k-means colors + AI palette)
2. Lokalny preview do swap'owania kolorów
3. Build image z `BUILD_BASE_PATH=/crm-{slug}`
4. Deploy do `dev.dokodu.it/crm-{slug}`
5. Załadowanie seed danych branżowych

Końcowy efekt: live demo URL gotowy do prezentacji dla klienta.

## KROK 1: Wyciągnij URL i slug

Z prompta użytkownika wyciągnij URL prospektu (np. `pedrollo.pl`, `https://haba.pl`).

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm exec tsx -e "import { slugFromUrl } from './scripts/lib/slug-from-url'; console.log(slugFromUrl(process.argv[1]))" -- "<URL>"
```

Wyświetl użytkownikowi: "Tworzę demo dla **{slug}** (URL: {url}). Szacowany czas: 4-6 minut."

## KROK 2: Generuj theme z URL

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
ANTHROPIC_API_KEY=$(cat ~/.config/anthropic_api_key 2>/dev/null) \
  pnpm theme:from-url <URL> 2>&1
```

Jeśli brak `~/.config/anthropic_api_key`:
- Spróbuj `~/.claude/anthropic_api_key`
- W ostateczności użyj `--skip-ai` (worse polish, ale działa)

Po zakończeniu: `themes/{slug}/theme.json` istnieje + `themes/{slug}/logo.{ext}`.

## KROK 3: Preview + tweak (interaktywnie)

```bash
pnpm theme:tweak <slug>
```

Otwiera browser na `http://localhost:3099`. Zapytaj użytkownika:
- "Otworzyłem podgląd theme'u. Akceptujesz kolory czy chcesz je doprecyzować przed deployem?"
- Jeśli akceptuje: kliknij "Save & exit" w UI lub `kill` proces tweak servera
- Jeśli chce zmieniać: powiedz mu żeby kliknął kolor, wybrał nowy, kliknął "Save & exit"

Czekaj aż proces tweak servera się zakończy (czyli plik został zapisany).

## KROK 4: Deploy na serwer

```bash
./scripts/deploy-instance.sh <slug> --bundle distribution-b2b
```

(Dla Pedrollo + HABA + similar dystrybucja: `--bundle distribution-b2b`. Dla innych: `--bundle generic` lub bez flagi.)

Skrypt:
1. Wgrywa theme + source na serwer
2. Buduje image (~2-3 min)
3. Migruje DB + ładuje seed
4. Startuje kontenery
5. Czeka na healthcheck
6. Wypisuje finalny URL

Jeśli skrypt zwróci błąd: pokaż użytkownikowi `ssh deploy@57.128.219.9 'cd /home/deploy/crm-instances/{slug} && docker compose -f docker-compose.{slug}.yml logs --tail 50'` — i zaproponuj debug.

## KROK 5: Smoke test + raport

```bash
SLUG=<slug>
curl -s -o /dev/null -w "%{http_code}\n" "https://dev.dokodu.it/crm-${SLUG}/api/health"
```

Oczekiwane: `200`.

Następnie wypisz raport dla użytkownika:

```
✅ DEMO READY

URL: https://dev.dokodu.it/crm-{slug}
Login: admin@dokodu.it / haslo z prisma seed (zwykle "admin123" — zmień po pierwszej prezentacji)

Co dostajesz w demie:
- 8 sample companies (industry: distribution-b2b)
- 8 deali w 5 etapach pipeline
- 16-24 aktywności (maile, telefony, spotkania)
- Theme z brandu {url}

Co dalej:
- Otwórz URL i przeklikaj
- Jeśli coś nie pasuje, edytuj manualnie w Prisma Studio: 
  ssh deploy@57.128.219.9 'cd /home/deploy/crm-instances/{slug} && docker compose -f docker-compose.{slug}.yml exec crm npx prisma studio'
- Po prezentacji: jeśli klient zaakceptował, /crm-fork-prospekt {slug} (Plan 3)
- Jeśli odrzucił: /crm-destroy-instance {slug}
```

## Uwagi techniczne

- Każda instancja ma własną bazę i własny container — ~250 MB RAM + 100 MB dysk per instancja
- TTL: zalecam ręczny destroy po 30 dniach jeśli klient nie wraca (Plan 3 doda auto-destroy)
- Browser cache: jeśli klient zobaczy starą wersję, hard reload Ctrl+Shift+R
````

- [ ] **Step 2: Verify BRAIN sees the new skill**

```bash
cd /Users/ksieradzinski/Projects/dokodu/brain-public
ls .claude/skills/crm-new-demo/
```

Expected: `SKILL.md` listed.

The skill is now invokable from any session by typing `/crm-new-demo {url}`.

- [ ] **Step 3: Commit**

```bash
cd /Users/ksieradzinski/Projects/dokodu/brain-public
git add .claude/skills/crm-new-demo/SKILL.md
git commit -m "feat(skill): /crm-new-demo orchestrator"
git push origin main
```

---

## Task 14: BRAIN skill `/crm-status`

**Why:** Quick way to see what's deployed, when, and whether it's healthy. Used during sales process management ("which prospects have demos right now?").

**Files:**
- Create: `~/Projects/dokodu/brain-public/.claude/skills/crm-status/SKILL.md`

- [ ] **Step 1: Write the skill**

````markdown
---
name: crm-status
description: Pokazuje status wszystkich aktywnych instancji CRM (master + per-prospekt + prod). Listuje slug, URL, status healthchecku, last deploy, container resource usage. Trigger: "status crm", "lista demo", "co stoi na crm", "które instancje", "/crm-status".
---

# Instrukcja: CRM Status

## KROK 1: Pobierz listę kontenerów

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
./scripts/list-instances.sh 2>&1
```

Skrypt zwraca JSON array — każdy obiekt ma `slug`, `name`, `status`, `image`.

## KROK 2: Per-instancja: healthcheck + age

Dla każdego slug w wynikach:

```bash
SLUG=<slug>
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "https://dev.dokodu.it/crm-${SLUG}/api/health" --max-time 5)
LAST_DEPLOY=$(ssh deploy@57.128.219.9 "stat -c %y /home/deploy/crm-instances/${SLUG}/docker-compose.${SLUG}.yml" 2>/dev/null || echo "n/a")
RESOURCE=$(ssh deploy@57.128.219.9 "docker stats crm-${SLUG} --no-stream --format 'CPU={{.CPUPerc}} MEM={{.MemUsage}}'" 2>/dev/null || echo "n/a")
```

## KROK 3: Wyświetl tabelę

```
INSTANCE              | STATUS | DEPLOYED            | RESOURCES
────────────────────────────────────────────────────────────────────
master                | ✅ 200 | 2026-04-15 12:30    | CPU=0.5% MEM=180MB / 8GB
crm-pedrollo          | ✅ 200 | 2026-04-28 17:42    | CPU=0.2% MEM=145MB / 8GB
crm-haba              | ❌ 502 | 2026-04-26 10:15    | down
────────────────────────────────────────────────────────────────────

Total: 3 instances, 2 healthy, 1 down.
```

Jeśli któraś instancja `down`:
- Powiedz: "Instancja {slug} jest nieosiągalna — sprawdź logi: `ssh deploy@57.128.219.9 'docker logs crm-{slug} --tail 50'`"
- Zaproponuj `/crm-destroy-instance {slug}` jeśli to martwa demo (>30 dni bez aktywności)
````

- [ ] **Step 2: Commit**

```bash
cd /Users/ksieradzinski/Projects/dokodu/brain-public
git add .claude/skills/crm-status/SKILL.md
git commit -m "feat(skill): /crm-status — list all CRM instances + health"
git push origin main
```

---

## Task 15: End-to-end smoke test (the real one — Pedrollo)

**Why:** Validates the entire pipeline works for a real prospect. After this task, Plan 2 is delivering value.

- [ ] **Step 1: Run /crm-new-demo for Pedrollo**

In a Claude Code session (any directory):

```
/crm-new-demo pedrollo.pl
```

Expected timeline:
- 0:00 — slug extraction → "pedrollo"
- 0:05 — start Playwright fetch
- 0:30 — fetch complete, start color extraction
- 0:35 — color/logo/font extraction done
- 0:38 — start AI polish (Claude Haiku, ~5s)
- 0:45 — theme.json written
- 0:50 — preview opens, you accept (or tweak + accept) within ~30s
- 1:30 — deploy script begins
- 4:00 — image build done
- 4:30 — migrations + seed
- 5:00 — containers up, healthcheck green
- 5:05 — DONE

Total ~5 min.

- [ ] **Step 2: Verify the demo**

Open `https://dev.dokodu.it/crm-pedrollo` in browser.

Checklist:
- [ ] Page loads with Pedrollo brand colors (red dominant per their site)
- [ ] Sidebar shows "Pedrollo CRM" name
- [ ] Login works with admin@dokodu.it / admin123
- [ ] Pipeline page shows 8 deals across 5 stages
- [ ] Companies page shows 8 sample companies (Hydro-Tech, Aquatech, etc.)
- [ ] Click any deal → drawer opens, activity timeline visible
- [ ] No console errors in browser DevTools

If any fails: capture issue, fix in source, re-deploy with `./scripts/deploy-instance.sh pedrollo --bundle distribution-b2b`. Iterate.

- [ ] **Step 3: Verify /crm-status shows the new instance**

```
/crm-status
```

Expected: Pedrollo instance listed with ✅ 200 health.

- [ ] **Step 4: Browser screenshot for documentation**

Capture 2-3 screenshots:
- Login page with Pedrollo brand
- Pipeline view with sample deals
- Open deal drawer

Save under `docs/superpowers/specs/2026-04-28-crm-demo-product-design/screenshots/pedrollo-demo-{1,2,3}.png` (in brain-public, NOT crm-new — these are reference/marketing).

```bash
mkdir -p /Users/ksieradzinski/Projects/dokodu/brain-public/docs/superpowers/specs/2026-04-28-crm-demo-product-design
# (drop screenshots manually)
cd /Users/ksieradzinski/Projects/dokodu/brain-public
git add docs/superpowers/specs/2026-04-28-crm-demo-product-design/
git commit -m "docs(crm): pedrollo demo screenshots"
git push origin main
```

- [ ] **Step 5: Final summary**

State to user:

```
🎉 PEDROLLO DEMO LIVE

URL: https://dev.dokodu.it/crm-pedrollo
Active until: manual destroy (use /crm-destroy-instance pedrollo)

Plan 2 delivered:
- theme-from-URL pipeline (Playwright + colors + logo + AI palette)
- tweak preview UI
- deploy/destroy/list scripts
- reverse-nginx routing for /crm-{slug}
- distribution-b2b seed bundle (Pedrollo-shaped data)
- BRAIN skille /crm-new-demo + /crm-status
- All Plan 1 follow-ups (middleware basePath, db import, .dockerignore, TODOs)

Co dalej:
- Plan 3: BRAIN operacyjne skille (fork-prospekt, migrate-to-prod, add-module, sync-from-master)
- Lub bezpośrednio: prezentacja Pedrollo + iteracja na demie + decyzja Phase 1 (fork) lub kill
```

---

## Final verification (after all 15 tasks done)

- [ ] **All tests pass**

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm test
```

Expected: ~50+ tests pass (Plan 1's 29 + new from Plan 2 ~25-30).

- [ ] **TypeScript clean**

```bash
pnpm exec tsc --noEmit
```

Expected: no NEW errors.

- [ ] **Production build (with prefix)**

```bash
DATABASE_URL=postgresql://test/test BASE_PATH=/crm-pedrollo pnpm build
```

Expected: success.

- [ ] **Docker build (with prefix)**

```bash
docker build --build-arg BUILD_BASE_PATH=/crm-pedrollo -t dokodu-crm:pedrollo .
docker rmi dokodu-crm:pedrollo
```

Expected: success.

- [ ] **Pedrollo demo live**

`https://dev.dokodu.it/crm-pedrollo` returns 200, shows branded demo with seed data.

- [ ] **Commit log clean**

```bash
git log --oneline main..HEAD
```

Expected: ~15 commits, focused, conventional commits style.

- [ ] **PR opened**

```bash
gh pr create --base main --title "feat(crm): theme-from-URL + Pedrollo demo (Plan 2/7)" --body-file <description>
```

---

## Out of scope (NEXT plans, NOT this one)

- BRAIN `/crm-fork-prospekt` skill (Plan 3) — fork instancji do osobnego repo gdy klient akceptuje demo
- BRAIN `/crm-migrate-to-prod` skill (Plan 3) — push z fork repo na klient serwer
- BRAIN `/crm-add-module` skill (Plan 3) — dodawanie modułów do istniejącej instancji
- BRAIN `/crm-update` skill (Plan 3) — rolling update istniejącej instancji
- BRAIN `/crm-sync-from-master` skill (Plan 3) — cherry-pick bug fix z mastera do klient repo
- HABA seed bundle (`water-treatment`) — odłożone do momentu konkretnej prezentacji u HABA
- Cmd+K AI parser (Plan 4)
- UX framework refresh (Plan 5)
- Bulletproof PII inventory (Plan 6)
- Reliability stack (Plan 7)

## Open questions surfaced during planning

1. **`crm-master` instancja** — czy potrzebujemy oddzielnego deploy mastera (`dev.dokodu.it/crm/`)? Moja sugestia: TAK, jako showroom „popatrzcie co potrafimy" przed konkretną prezentacją per klient. Można dodać jako Task 16 albo zrobić ad-hoc po Plan 2.

2. **Cleanup automation** — instancje mnożą się; przydałby się cron job „destroy instances older than 30 days with no traffic". Plan 3 candidate.

3. **Builds on server vs local** — Task 10 buduje image NA SERWERZE (rsync source + docker build). Alternatywa: build lokalnie + push do private registry (Docker Hub Pro / GHCR). Wybrałem build-on-server bo: prostsze (brak registry), brak transferu image (~700 MB). Wada: build CPU obciąża serwer Dokodu. Akceptowalne dla 5-10 demo równolegle. Re-evaluate przy 50+ demo.

4. **`logoDarkUrl` w theme** — Plan 2 nie generuje variant'u dla dark mode. Plan 5 (UX refresh + dark mode) doda. Nazwa pola jest w schemacie (Plan 1) — fine.

5. **Bundle name na URL** — Plan 2 dispatcher czyta `SEED_BUNDLE` env w migrate container. Co jeśli ktoś zapomni `--bundle` flag? Skrypt po prostu nie odpali bundle'a — instancja będzie pusta poza default seed. To jest OK (default zachowanie) ale warto wspomnieć w docs.
